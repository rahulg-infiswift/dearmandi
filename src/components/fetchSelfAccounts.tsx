// Interface for an individual account
interface Account {
  id: string;
  name: string;
  // Add other account properties as needed
}

async function fetchSelfAccounts(token: string): Promise<Array<Account>> {
  try {
    const response = await fetch("/api/accounts/self_accounts", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data: Array<Account> = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch self accounts:", error);
    throw error; // Re-throw the error to handle it where the function is called
  }
}

export default fetchSelfAccounts;
