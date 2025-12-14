"use client"

import React from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { signupSchema, type SignupInput } from "../../../../schemas/authSchema"
import { Form, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { signIn } from "next-auth/react"

export default function SignupPage() {
	const router = useRouter()
	const form = useForm<SignupInput>({ resolver: zodResolver(signupSchema) })

	async function onSubmit(values: SignupInput) {
		try {
			const res = await fetch("/api/auth/signup", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(values),
			})
			const data = await res.json()
			if (!res.ok) {
				toast.error(data.error || "Signup failed")
				return
			}

			// auto sign in after signup
			const signRes = await signIn("credentials", {
				redirect: true,
				email: values.email,
				password: values.password,
				callbackUrl: "/",
			} as any)

			// if signIn redirected, nothing else to do; otherwise push
			router.push("/")
		} catch (err: any) {
			toast.error(err?.message || "Unexpected error")
		}
	}

	return (
		<div className="mx-auto max-w-md p-6">
			<h1 className="text-2xl font-semibold mb-4">Create account</h1>
			<Form {...form}>
				<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
					<FormItem>
						<FormLabel>Username</FormLabel>
						<FormControl>
							<Input placeholder="username" {...form.register("username")} />
						</FormControl>
						<FormMessage>{form.formState.errors.username?.message}</FormMessage>
					</FormItem>

					<FormItem>
						<FormLabel>Email</FormLabel>
						<FormControl>
							<Input type="email" placeholder="you@example.com" {...form.register("email")} />
						</FormControl>
						<FormMessage>{form.formState.errors.email?.message}</FormMessage>
					</FormItem>

					<FormItem>
						<FormLabel>Password</FormLabel>
						<FormControl>
							<Input type="password" placeholder="Password" {...form.register("password")} />
						</FormControl>
						<FormMessage>{form.formState.errors.password?.message}</FormMessage>
					</FormItem>

					<Button type="submit">Sign up</Button>
				</form>
			</Form>
		</div>
	)
}
