export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id?: number;
  created_at: string;
  updated_at?: string;
  promptCount?: number;
}

export interface Tag {
  id: number;
  name: string;
  created_at: string;
  updated_at?: string;
  promptCount?: number;
}

export interface Prompt {
  id: number;
  title: string;
  content: string;
  description?: string;
  is_public: boolean;
  owner_id: number;
  category_id?: number;
  category?: Category;
  tags: Tag[];
  usageCount: number;
  likeCount: number;
  shareCount: number;
  created_at: string;
  updated_at?: string;
} 