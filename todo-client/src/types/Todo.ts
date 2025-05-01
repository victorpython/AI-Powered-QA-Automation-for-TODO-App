export interface Todo {
    id: number;
    title: string;
    isCompleted: boolean;
    createdAt: string;
    category: string;
}

export const categories = [
    "Work",
    "Personal",
    "Shopping",
    "Health",
    "Important",
    "Study"
] as const;

export type Category = typeof categories[number];
