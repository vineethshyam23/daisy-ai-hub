export interface AIComponent {
  id: string
  name: string
  description: string
  category: string
  icon: string
  color: string
  component: string
  route: string
  tags: string[]
  featured?: boolean
  isNew?: boolean
}

export interface AICategory {
  id: string
  name: string
  description: string
  icon: string
  color: string
}

export interface ConfluenceSearchResult {
  id: string
  title: string
  excerpt: string
  url: string
  space: string
  lastModified: string
  type: 'page' | 'blogpost' | 'attachment'
}

export interface ImageGenerationRequest {
  prompt: string
  style?: 'realistic' | 'artistic' | 'cartoon' | 'abstract'
  size?: '256x256' | '512x512' | '1024x1024'
  count?: number
}

export interface GeneratedImage {
  id: string
  url: string
  prompt: string
  createdAt: string
} 