"use client";

import Link from "next/link";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav
      style={{
        padding: "16px",
        borderBottom: "1px solid #ccc",
        display: "flex",
        gap: "20px",
      }}
    >
      <Link href="/">Home</Link>

      {!isAuthenticated ? (
        <>
          <Link href="/login">Login</Link>
          <Link href="/register">Register</Link>
        </>
      ) : (
        <>
          <Link href="/upload">Upload</Link>

          <button onClick={logout}>
            Logout
          </button>
        </>
      )}
    </nav>
  );
}
