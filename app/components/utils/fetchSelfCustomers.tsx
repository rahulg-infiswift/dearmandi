// Interface for an individual account
interface Customer {
  id: string;
  name: string;
  // Add other account properties as needed
}

async function fetchSelfCustomers(token: string): Promise<Array<Customer>> {
  try {
    const response = await fetch("/api/customers/self_customers", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data: Array<Customer> = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch self customers:", error);
    throw error; // Re-throw the error to handle it where the function is called
  }
}

export default fetchSelfCustomers;
