import { z } from "zod";

export const createPostSchema = z.object({
	imageUrl: z.string().url("Image URL must be a valid URL"),
	caption: z.string().max(2200).optional(),
});

export type CreatePostInput = z.infer<typeof createPostSchema>;
