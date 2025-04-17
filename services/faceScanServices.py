from repository.userRepository import UpdateEmbedding, GetEmbedding
from facenet_pytorch import InceptionResnetV1
import torch.nn.functional as F
from torchvision import transforms
import torch
from PIL import Image
import numpy as np
import json
import base64
import io

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model = InceptionResnetV1(pretrained='vggface2').to(device).eval()
torch.manual_seed(42)

print(f"Using device: {device}")

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4),
    transforms.RandomRotation(degrees=10),
    transforms.RandomAffine(degrees=0, translate=(0.02, 0.02), scale=(0.95, 1.05)),
    transforms.RandomPerspective(distortion_scale=0.3, p=0.5),
    transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
    transforms.ToTensor(),
    transforms.RandomErasing(p=0.3, scale=(0.02, 0.1), ratio=(0.3, 3.3), value='random'),
])

def cosine_similarity(emb1, emb2):
    emb1 = torch.tensor(emb1)
    emb2 = torch.tensor(emb2)
    return F.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0)).item()

def generateEmbedding(faces_base64):
    print("Decoding base64 strings")
    images = [
        Image.open(io.BytesIO(base64.b64decode(data))).resize((256, 256))
        for data in faces_base64[:3]
    ]

    print("Converting images to raw tensors")
    raw_tensors = [
        torch.tensor(np.array(img) / 255.).permute(2, 0, 1).unsqueeze(0).float()
        for img in images
    ]

    print("Applying data augmentation")
    augmented_tensors = []
    augmented_num_per_img = 40
    for img in images:
        augmented_tensors.extend([
            transform(img).unsqueeze(0).float()
            for _ in range(augmented_num_per_img)
        ])

    print("Combining all tensors")
    all_tensors = raw_tensors + augmented_tensors

    print("Generating embeddings")
    with torch.no_grad():
        embeddings = [model(tensor.to(device)) for tensor in all_tensors]

    np_embeddings = [embedding.cpu().numpy().flatten() for embedding in embeddings]
    embedding_median = np.median(np_embeddings, axis=0)
    embedding_list = np.round(embedding_median, 3).tolist()
    embedding_str = json.dumps(embedding_list)

    return embedding_str

def StoreEmbedding(username, faces_base64):
    embedding_str = generateEmbedding(faces_base64)

    res = UpdateEmbedding(username, embedding_str)

    if res == 0:
        return False
    
    return True

def ConvertB64Embedding(face_base64):
    print("decoding base64 string")
    image_data = base64.b64decode(face_base64)
    img = Image.open(io.BytesIO(image_data)).resize((256, 256))

    print("converting images to tensors")
    img_tensor = torch.tensor(np.array(img) / 255.).permute(2, 0, 1).unsqueeze(0).float()

    print("generating embeddings")
    with torch.no_grad():
        embedding = model(img_tensor.to(device))

    np_embedding = embedding.cpu().numpy().flatten()
    return np_embedding

def CompareEmbedding(username, face_base64):
    res = GetEmbedding(username)

    if res == 0:
        return False, 0
    
    storedEmbedding = json.loads(res)
    embedding = ConvertB64Embedding(face_base64)

    matches = cosine_similarity(storedEmbedding, embedding)

    if matches < 0.85:
        return False, np.round(matches, 3)*100

    return True, np.round(matches, 3)*100