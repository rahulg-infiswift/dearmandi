const signupFunction = async (
  name: string,
  email: string,
  password: string
) => {
  try {
    const response = await fetch("/api/users/create_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password: password,
      }),
    });
    if (!response.ok) {
      throw new Error("Signup failed");
    }
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("Signup failed:", error);
    return null;
  }
};

export default signupFunction;