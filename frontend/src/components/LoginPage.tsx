"use client";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import axios from "axios";

export const description =
  "A login form with email and password. There's an option to login with Google and a link to sign up if you don't have an account.";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState(""); // To display success or error messages
  const router = useRouter(); // For navigation after successful login

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent the default form submission

    const params = new URLSearchParams({
      username: email, // OAuth2PasswordRequestForm expects 'username' as the key, not 'email'
      password: password,
    });

    try {
      const response = await axios.post("/api/auth/token", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Set the correct content type
        },
      });

      // If the login is successful, store the token and navigate to the home page
      const { access_token } = response.data;
      localStorage.setItem("token", access_token); // Store the token in localStorage (or use cookies if needed)
      setMessage("Login successful!");

      // Redirect the user to the dashboard or home page after successful login
      router.push("/home");
    } catch (error: any) {
      console.log(error.response);
      if (error.response && error.response.status === 401) {
        // If the status is 401 Unauthorized, display a specific message
        setMessage("Invalid email or password. Please try again.");
      } else if (error.response && error.response.status === 403) {
        // Handle unverified email
        setMessage("Your email is not verified. Please check your inbox.");
      } else {
        // For other errors, display a generic error message
        setMessage("Login failed. Please check your credentials.");
      }
    }
  };

  return (
    <Card className="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle className="text-2xl">Login</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="rahulgarg@example.com"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                <Link
                  href="#"
                  className="ml-auto inline-block text-sm underline"
                >
                  Forgot your password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <Button type="submit" className="w-full">
              Login
            </Button>
            <Button variant="outline" className="w-full">
              Login with Google
            </Button>
          </div>
        </form>
        {message && (
          <div className="mt-4 text-center text-sm text-red-500">{message}</div>
        )}
        <div className="mt-4 text-center text-sm">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="underline">
            Sign up
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
