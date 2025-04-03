from repository.userRepository import UpdateEmbedding, GetEmbedding
from facenet_pytorch import InceptionResnetV1
import torch.nn.functional as F
import torch
from PIL import Image
import numpy as np
import json
import base64
import io

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model = InceptionResnetV1(pretrained='vggface2').to(device).eval()

def cosine_similarity(emb1, emb2):
    emb1 = torch.tensor(emb1)
    emb2 = torch.tensor(emb2)
    return F.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0)).item()

def generateEmbedding(faces_base64):
    print("decoding base64 strings")
    image_data_1 = base64.b64decode(faces_base64[0])
    image_data_2 = base64.b64decode(faces_base64[1])
    image_data_3 = base64.b64decode(faces_base64[2])

    img1 = Image.open(io.BytesIO(image_data_1)).resize((256, 256))
    img2 = Image.open(io.BytesIO(image_data_2)).resize((256, 256))
    img3 = Image.open(io.BytesIO(image_data_3)).resize((256, 256))

    print("converting images to tensors")
    img1_tensor = torch.tensor(np.array(img1) / 255.).permute(2, 0, 1).unsqueeze(0).float()
    img2_tensor = torch.tensor(np.array(img2) / 255.).permute(2, 0, 1).unsqueeze(0).float()
    img3_tensor = torch.tensor(np.array(img3) / 255.).permute(2, 0, 1).unsqueeze(0).float()

    print("generating embeddings")
    with torch.no_grad():
        embedding1 = model(img1_tensor.to(device))
        embedding2 = model(img2_tensor.to(device))
        embedding3 = model(img3_tensor.to(device))

    np_embedding1 = embedding1.cpu().numpy().flatten()
    np_embedding2 = embedding2.cpu().numpy().flatten()
    np_embedding3 = embedding3.cpu().numpy().flatten()

    embedding_median = np.median([np_embedding1, np_embedding2, np_embedding3], axis=0).flatten()
    embedding_list = np.round(embedding_median.flatten(), 3).tolist()
    embedding_str = json.dumps(embedding_list)

    return embedding_str

def StoreEmbedding(username, faces_base64):
    embedding_str = generateEmbedding(faces_base64)

    res = UpdateEmbedding(username, embedding_str)

    if res == 0:
        return False
    
    return True