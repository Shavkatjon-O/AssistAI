"use client"

import axios from "axios"
// import { useEffect, useState } from "react"
import Cookies from "js-cookie"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function SignInPage() {
  const onSubmitHandler = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const username = (event.currentTarget.elements.namedItem("username") as HTMLInputElement).value
    const password = (event.currentTarget.elements.namedItem("password") as HTMLInputElement).value

    if (username && password) {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/admin/token`, {
        username: username,
        password: password,
      })

      if (response.status === 200) {
        const token = response.data.access_token
        Cookies.set("access_token", token)
        console.log(token)
        window.location.href = "/admin"
      }
    }
  }

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <div className="flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Sign In</CardTitle>
              <CardDescription>
                Enter your username below to sign in to your account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={onSubmitHandler}>
                <div className="flex flex-col gap-6">
                  <div className="grid gap-2">
                    <Label htmlFor="username">Username</Label>
                    <Input
                      id="username"
                      type="text"
                      placeholder="Enter your username"
                      className="h-12"
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="password">Password</Label>
                    <Input 
                      id="password"
                      type="password"
                      placeholder="Enter your password"
                      className="h-12" 
                      required 
                    />
                  </div>
                  <Button type="submit" className="w-full h-12">
                    Sign In
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
