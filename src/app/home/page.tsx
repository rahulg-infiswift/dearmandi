"use client";

import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react'

function Page() {
  const router = useRouter();

  useEffect(() => {
    // Check if the token exists in localStorage
    const token = localStorage.getItem("token");

    // If no token is found, redirect to the login page
    if (!token) {
      router.push("/home/dashboard");
    }
  }, [router]);

  return null;
}

export default Page
