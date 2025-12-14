"use client"

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Postcard from "@/components/Postcard";

export default function PostDetailPage() {
	const params = useParams();
	const id = (params as any)?.id;
	const [post, setPost] = useState<any | null>(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		if (!id) return;
		setLoading(true);
		fetch(`/api/post/${id}`)
			.then((r) => r.json())
			.then((data) => {
				if (data?.post) setPost(data.post);
			})
			.catch(() => {})
			.finally(() => setLoading(false));
	}, [id]);

	if (loading) return <div className="p-6"><div className="rounded bg-card p-6 animate-pulse">&nbsp;</div></div>;
	if (!post) return <div className="p-6">Post not found</div>;

	return (
		<div className="mx-auto max-w-3xl p-6">
			<div className="mb-4">
				<h1 className="text-xl font-semibold">Post</h1>
			</div>
			<Postcard post={post} />
		</div>
	);
}
