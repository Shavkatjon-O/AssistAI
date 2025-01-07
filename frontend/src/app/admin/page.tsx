"use client";
import coreApi from "@/lib/coureApi"
import { useEffect, useState } from "react";

interface Profile {
  username: string;
  id: number;
}

export default function Page() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [isLoaded, setIsLoaded] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    coreApi
      .get("/admin/me")
      .then((response) => {
        setProfile(response.data);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsLoaded(true);
      });
  }, []);

  return (
    <div>
      {
        isLoaded ? (
          error ? (
            <p>Error: {error}</p>
          ) : (
            <div>
              <p>Username: {profile?.username}</p>
              <p>ID: {profile?.id}</p>
            </div>
          )
        ) : (
          <p>Loading...</p>
        )
      }
    </div>
  );
};