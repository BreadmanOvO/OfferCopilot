import { CompanyJobsResponse, TaskResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export async function createTask(payload: Record<string, unknown>): Promise<TaskResponse> {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<TaskResponse>(response);
}

export async function getTask(taskId: string): Promise<TaskResponse> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}`, { cache: "no-store" });
  return handleResponse<TaskResponse>(response);
}

export async function appendInputs(taskId: number, payload: Record<string, unknown>): Promise<TaskResponse> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}/inputs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<TaskResponse>(response);
}

export async function runTask(taskId: number): Promise<TaskResponse> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}/run`, { method: "POST" });
  return handleResponse<TaskResponse>(response);
}

export async function sendFollowUp(taskId: number, question: string): Promise<{ answer: string }> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}/follow-up`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse<{ answer: string }>(response);
}

export async function getCompanyJobs(companyName: string): Promise<CompanyJobsResponse> {
  const response = await fetch(
    `${API_BASE}/tasks/jobs/${encodeURIComponent(companyName)}`
  );
  return handleResponse<CompanyJobsResponse>(response);
}
