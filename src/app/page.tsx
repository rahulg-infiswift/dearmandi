"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      // Redirect to dashboard if authenticated
      router.push("/home");
    } else {
      // Redirect to login if not authenticated
      router.push("/login");
    }
  }, [router]);

  return null;
}
