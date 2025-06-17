import { ResetPasswordPage } from "@/components/ResetPasswordPage";
import React, { Suspense } from "react";

// Loading component to show while the ResetPasswordPage is loading
const ResetPasswordLoading = () => (
  <div className="h-screen flex justify-center items-center">
    <p>Loading reset password form...</p>
  </div>
);

const page = () => {
  return (
    <div className="h-screen flex justify-center items-center">
      <Suspense fallback={<ResetPasswordLoading />}>
        <ResetPasswordPage />
      </Suspense>
    </div>
  );
};

export default page;
