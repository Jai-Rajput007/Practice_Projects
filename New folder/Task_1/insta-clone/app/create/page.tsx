"use client"

import React from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { createPostSchema, type CreatePostInput } from "../../schemas/postSchema";
import { Form, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function CreatePage() {
	const router = useRouter();
	const form = useForm<CreatePostInput>({ resolver: zodResolver(createPostSchema) });

	async function onSubmit(values: CreatePostInput) {
		try {
			const res = await fetch("/api/posts", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values) });
			const data = await res.json();
			if (!res.ok) {
				toast.error(data.error || "Failed to create post");
				return;
			}
			toast.success("Post created");
			router.push("/");
		} catch (e: any) {
			toast.error(e?.message || "Error");
		}
	}

	return (
		<div className="mx-auto max-w-md p-6">
			<Card>
				<CardHeader>
					<CardTitle>Create Post</CardTitle>
				</CardHeader>
				<CardContent>
					<Form {...form}>
						<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
							<FormItem>
								<FormLabel>Image URL</FormLabel>
								<FormControl>
									<Input placeholder="https://..." {...form.register("imageUrl")} />
								</FormControl>
								<FormMessage>{form.formState.errors.imageUrl?.message}</FormMessage>
							</FormItem>

							<FormItem>
								<FormLabel>Caption</FormLabel>
								<FormControl>
									<textarea className="w-full rounded border px-3 py-2" {...form.register("caption")} />
								</FormControl>
								<FormMessage>{form.formState.errors.caption?.message}</FormMessage>
							</FormItem>

							<div className="flex justify-end">
								<Button type="submit">Create</Button>
							</div>
						</form>
					</Form>
				</CardContent>
			</Card>
		</div>
	);
}
