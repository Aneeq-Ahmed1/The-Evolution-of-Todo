"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to tasks page
    router.replace("/dashboard/tasks");
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold">Loading...</h2>
        <p className="text-gray-600 mt-2">Redirecting to your tasks</p>
      </div>
    </div>
  );
}
