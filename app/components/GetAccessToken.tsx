
const GetAccessToken = async (username: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  try {
    console.log(username, password);
    const response = await fetch("/api/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });
    if (!response.ok) {
      throw new Error("Login failed");
    }
    const { access_token } = await response.json();
    // Store the token in localStorage or cookies
    console.log("token", access_token);
    localStorage.setItem("token", access_token); // Store the token
    return access_token;
  } catch (error) {
    console.error("Login failed:", error);
    return null;
  }
};

export default GetAccessToken;
