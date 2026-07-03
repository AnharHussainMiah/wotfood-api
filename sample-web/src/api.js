export async function postJson(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // Handle HTTP errors (4xx, 5xx)
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Request failed (${response.status}): ${errorText || response.statusText}`
      );
    }

    // Parse JSON response
    const result = await response.json();
    return result;

  } catch (error) {
    console.error("POST request failed:", error);
    throw error; // Re-throw if the caller should handle it
  }
}