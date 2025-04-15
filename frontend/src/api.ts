import axios from "axios";

export interface Summary {
  title: string;
  key_points: string[];
  action_items: string[];
}

export interface UploadResponse {
  id: string;
  status: string;
}

export async function uploadFile(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post("/api/upload", formData);

  return res.data;
}

export async function startAnalysis(id: string): Promise<void> {
  await axios.post("/api/analyse", { id });
}

export async function fetchResults(id: string): Promise<{
  status: string;
  summary?: Summary;
}> {
  const res = await axios.get(`/api/results/${id}`);
  return res.data;
}