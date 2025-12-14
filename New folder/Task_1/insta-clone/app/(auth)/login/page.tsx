"use client"

import React from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { loginSchema, type LoginInput } from "../../../../schemas/authSchema"
import { Form, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { signIn } from "next-auth/react"
import { toast } from "sonner"

export default function LoginPage() {
	const router = useRouter()
	const form = useForm<LoginInput>({ resolver: zodResolver(loginSchema) })

	async function onSubmit(values: LoginInput) {
		try {
			const res = await signIn("credentials", { redirect: false, ...values } as any)
			if (res && (res as any).error) {
				toast.error((res as any).error || "Invalid credentials")
				return
			}
			router.push("/")
		} catch (err: any) {
			toast.error(err?.message || "Login error")
		}
	}

	return (
		<div className="mx-auto max-w-md p-6">
			<h1 className="text-2xl font-semibold mb-4">Sign in</h1>
			<Form {...form}>
				<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
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

					<Button type="submit">Sign in</Button>
				</form>
			</Form>
		</div>
	)
}

