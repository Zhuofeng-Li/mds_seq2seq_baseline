from huggingface_hub import hf_hub_download

# Download the file
file_path = hf_hub_download(repo_id="ZhuofengLi/MDS", filename="test.csv", repo_type="dataset", local_dir=".")

print(f"File downloaded to {file_path}")