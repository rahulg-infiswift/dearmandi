"use client";

import { DashboardPage } from '@/components/DashboardPage'
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react'

function page() {
  const router = useRouter();

  useEffect(() => {
    // Check if the token exists in localStorage
    const token = localStorage.getItem("token");

    // If no token is found, redirect to the login page
    if (!token) {
      router.push("/");
    }
  }, [router]);

  return (
    <div>
      <DashboardPage />
    </div>
  )
}

export default page
