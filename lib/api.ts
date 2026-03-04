export interface FetchOptions extends RequestInit {
  token?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchAPI<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: HeadersInit = {
    ...(fetchOptions.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...fetchOptions,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_email");
        window.location.href = "/login";
      }

      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error: ${response.status}`);
    }

    // Handle empty responses (like 204 No Content)
    if (response.headers.get("content-length") === "0") {
      return {} as T;
    }

    return response.json();
  } catch (error) {
    console.error("[v0] API call failed:", {
      endpoint,
      apiUrl: API_URL,
      error: error instanceof Error ? error.message : String(error),
    });
    throw error;
  }
}

export async function postAPI<T>(
  endpoint: string,
  data: unknown,
  token?: string
): Promise<T> {
  return fetchAPI<T>(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    token,
  });
}

export async function postFormData<T>(
  endpoint: string,
  formData: FormData,
  token?: string
): Promise<T> {
  return fetchAPI<T>(endpoint, {
    method: "POST",
    body: formData,
    token,
  });
}

export async function getAPI<T>(
  endpoint: string,
  token?: string
): Promise<T> {
  return fetchAPI<T>(endpoint, {
    method: "GET",
    token,
  });
}
