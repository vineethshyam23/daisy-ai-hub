import { useAuthStore } from '~/stores/auth'

interface GitLabUser {
  id: number
  username: string
  name: string
  email: string
  avatar_url: string
  web_url: string
}

interface GitLabProject {
  id: number
  name: string
  name_with_namespace: string
  description: string
  web_url: string
  ssh_url_to_repo: string
  http_url_to_repo: string
  visibility: string
  default_branch: string
  created_at: string
  updated_at: string
}

interface GitLabRepository {
  id: number
  name: string
  path: string
  kind: string
}

export const useGitLab = () => {
  const authStore = useAuthStore()
  const baseURL = 'https://gitlab.com/api/v4'

  const makeRequest = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
    const token = await authStore.getGitLabAccessToken()
    
    if (!token) {
      throw new Error('GitLab access token not found. Please login with GitLab first.')
    }

    const response = await fetch(`${baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`GitLab API error: ${response.status} ${response.statusText}`)
    }

    return response.json()
  }

  // Get current user profile
  const getCurrentUser = async (): Promise<GitLabUser> => {
    return makeRequest<GitLabUser>('/user')
  }

  // Get user projects
  const getUserProjects = async (options: {
    owned?: boolean
    membership?: boolean
    starred?: boolean
    per_page?: number
    page?: number
  } = {}): Promise<GitLabProject[]> => {
    const params = new URLSearchParams()
    
    if (options.owned) params.append('owned', 'true')
    if (options.membership) params.append('membership', 'true')
    if (options.starred) params.append('starred', 'true')
    if (options.per_page) params.append('per_page', options.per_page.toString())
    if (options.page) params.append('page', options.page.toString())

    const queryString = params.toString()
    const endpoint = queryString ? `/projects?${queryString}` : '/projects'
    
    return makeRequest<GitLabProject[]>(endpoint)
  }

  // Get specific project
  const getProject = async (projectId: number | string): Promise<GitLabProject> => {
    return makeRequest<GitLabProject>(`/projects/${projectId}`)
  }

  // Get project repositories/tree
  const getProjectRepository = async (
    projectId: number | string, 
    path: string = '', 
    ref: string = 'main'
  ): Promise<GitLabRepository[]> => {
    const params = new URLSearchParams()
    if (path) params.append('path', path)
    if (ref) params.append('ref', ref)
    
    const queryString = params.toString()
    const endpoint = queryString 
      ? `/projects/${projectId}/repository/tree?${queryString}`
      : `/projects/${projectId}/repository/tree`
    
    return makeRequest<GitLabRepository[]>(endpoint)
  }

  // Get file content
  const getFileContent = async (
    projectId: number | string,
    filePath: string,
    ref: string = 'main'
  ): Promise<{ content: string; encoding: string }> => {
    const encodedPath = encodeURIComponent(filePath)
    return makeRequest(`/projects/${projectId}/repository/files/${encodedPath}?ref=${ref}`)
  }

  // Check if user has GitLab access
  const hasGitLabAccess = computed(() => {
    return authStore.hasGitLabToken
  })

  return {
    // API methods
    getCurrentUser,
    getUserProjects,
    getProject,
    getProjectRepository,
    getFileContent,
    
    // Utilities
    hasGitLabAccess,
    makeRequest,
  }
} 