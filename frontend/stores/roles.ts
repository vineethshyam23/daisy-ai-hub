import { defineStore } from 'pinia'
import { doc, getDoc, setDoc, collection, getDocs, serverTimestamp } from 'firebase/firestore'
import { useAuthStore } from './auth'

// Role definitions
export type UserRole = 'admin' | 'standard'

// Central list of all available assistants
export const ALL_ASSISTANTS = [
  'email-responder',
  'social-media-generator', 
  'image-generator',
  'meeting-summarizer',
  'approved-metro-tools',
  'document-processor',
  'invoice-validator-sco',
  'multi-document-analyzer',
  'learning-path-creator'
] as const

export interface UserRoleData {
  email: string
  role: UserRole
  assignedBy: string
  assignedAt: any
  isActive: boolean
}

export interface RolePermissions {
  roleName: UserRole
  displayName: string
  allowedAssistants: string[]
  dailyTokenLimit: number
  description: string
}

// Emergency fallback roles (only used if Firebase is completely unavailable)
const EMERGENCY_FALLBACK_ROLES: Record<UserRole, RolePermissions> = {
  admin: {
    roleName: 'admin',
    displayName: 'Administrator',
    allowedAssistants: [...ALL_ASSISTANTS], // All assistants available for admin
    dailyTokenLimit: 100,
    description: 'Emergency fallback admin role'
  },
  standard: {
    roleName: 'standard',
    displayName: 'Standard User',
    allowedAssistants: [...ALL_ASSISTANTS], // All assistants available for standard users too
    dailyTokenLimit: 50,
    description: 'Emergency fallback standard role'
  }
}

export const useRoleStore = defineStore('roles', () => {
  const db = useFirestore()
  const authStore = useAuthStore()
  
  // State
  const userRole = ref<UserRole | null>(null)
  const rolePermissions = ref<RolePermissions | null>(null)
  const isLoading = ref(false)
  const isInitialized = ref(false)
  const allRolePermissions = ref<Record<string, RolePermissions>>({})

  // Computed
  const isAdmin = computed(() => userRole.value === 'admin')
  const canAccessAssistant = computed(() => (assistantName: string) => {
    if (!rolePermissions.value) return false
    return rolePermissions.value.allowedAssistants.includes(assistantName)
  })
  const dailyTokenLimit = computed(() => rolePermissions.value?.dailyTokenLimit || 50)

  // Load user role from Firestore
  const loadUserRole = async (): Promise<UserRole | null> => {
    if (!authStore.user?.uid) return null

    try {
      const userRoleRef = doc(db, 'userRoles', authStore.user.uid)
      const userRoleDoc = await getDoc(userRoleRef)
      
      if (userRoleDoc.exists()) {
        const roleData = userRoleDoc.data() as UserRoleData
        if (roleData.isActive) {
          return roleData.role
        }
      }
      
      // If no role assigned, assign default standard role
      return await assignDefaultRole()
    } catch (error) {
      console.error('Error loading user role:', error)
      return 'standard' // Fallback to basic role
    }
  }

  // Assign default role to new user
  const assignDefaultRole = async (): Promise<UserRole> => {
    if (!authStore.user?.uid || !authStore.user?.email) return 'standard'

    try {
      const defaultRole: UserRole = 'standard'
      const roleData: UserRoleData = {
        email: authStore.user.email,
        role: defaultRole,
        assignedBy: 'system',
        assignedAt: serverTimestamp(),
        isActive: true
      }

      const userRoleRef = doc(db, 'userRoles', authStore.user.uid)
      await setDoc(userRoleRef, roleData)
      
      return defaultRole
    } catch (error) {
      console.warn('Could not assign default role (insufficient permissions), using standard role:', error)
      return 'standard'
    }
  }

  // Load role permissions from Firebase
  const loadRolePermissions = async (role: UserRole): Promise<RolePermissions | null> => {
    try {
      const roleRef = doc(db, 'rolePermissions', role)
      const roleDoc = await getDoc(roleRef)
      
      if (roleDoc.exists()) {
        const permissions = roleDoc.data() as RolePermissions
        return permissions
      }
      
      console.warn(`⚠️ No permissions found in Firebase for role: ${role}`)
      return null
    } catch (error) {
      console.error(`❌ Error loading role permissions for ${role}:`, error)
      return null
    }
  }

  // Load all role permissions (for admin interface)
  const loadAllRolePermissions = async () => {
    try {
      const rolePermissionsRef = collection(db, 'rolePermissions')
      const snapshot = await getDocs(rolePermissionsRef)
      
      const permissions: Record<string, RolePermissions> = {}
      snapshot.forEach(doc => {
        permissions[doc.id] = doc.data() as RolePermissions
      })
      allRolePermissions.value = permissions
      
      return permissions
    } catch (error) {
      console.error('❌ Error loading all role permissions:', error)
      return {}
    }
  }

  // Assign role to user (admin only)
  const assignRole = async (userId: string, email: string, role: UserRole): Promise<boolean> => {
    if (!isAdmin.value || !authStore.user?.uid) {
      throw new Error('Only admins can assign roles')
    }

    try {
      const roleData: UserRoleData = {
        email,
        role,
        assignedBy: authStore.user.uid,
        assignedAt: serverTimestamp(),
        isActive: true
      }

      const userRoleRef = doc(db, 'userRoles', userId)
      await setDoc(userRoleRef, roleData)
      
      return true
    } catch (error) {
      console.error('Error assigning role:', error)
      return false
    }
  }

  // Get role display name
  const getRoleDisplayName = (role: UserRole): string => {
    // Try to get from loaded permissions first
    const rolePermissions = allRolePermissions.value[role]
    if (rolePermissions?.displayName) {
      return rolePermissions.displayName
    }
    
    // Fallback to emergency roles
    return EMERGENCY_FALLBACK_ROLES[role]?.displayName || role
  }

  // Check if user has permission for specific assistant
  const hasAssistantPermission = (assistantName: string): boolean => {
    if (!isInitialized.value || !rolePermissions.value) return false
    if (!Array.isArray(rolePermissions.value.allowedAssistants)) return false
    
    return rolePermissions.value.allowedAssistants.includes(assistantName)
  }

  // Initialize role system
  const init = async () => {
    if (isInitialized.value || !authStore.isAuthenticated) return

    isLoading.value = true
    
    try {
      
      // Load user role
      const role = await loadUserRole()
      
      if (role) {
        userRole.value = role
        
        // Load permissions for user role
        const permissions = await loadRolePermissions(role)
        
        if (permissions) {
          rolePermissions.value = permissions
        } else {
          // Use emergency fallback
          console.warn(`⚠️ Using emergency fallback permissions for role: ${role}`)
          rolePermissions.value = EMERGENCY_FALLBACK_ROLES[role]
        }
        
        // Load all permissions if admin
        if (role === 'admin') {
          await loadAllRolePermissions()
        }
      } else {
        // Fallback if no role could be determined
        console.warn('⚠️ No role determined, using standard role fallback')
        userRole.value = 'standard'
        rolePermissions.value = EMERGENCY_FALLBACK_ROLES['standard']
      }
      
      isInitialized.value = true 
      
    } catch (error) {
      console.error('❌ Critical error initializing role store:', error)
      // Ensure we have at least basic functionality
      userRole.value = 'standard'
      rolePermissions.value = EMERGENCY_FALLBACK_ROLES['standard']
      isInitialized.value = true
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    userRole: readonly(userRole),
    rolePermissions: readonly(rolePermissions),
    isLoading: readonly(isLoading),
    isInitialized: readonly(isInitialized),
    allRolePermissions: readonly(allRolePermissions),
    
    // Computed
    isAdmin,
    canAccessAssistant,
    dailyTokenLimit,
    
    // Methods
    init,
    loadUserRole,
    assignRole,
    getRoleDisplayName,
    hasAssistantPermission,
    loadAllRolePermissions,
    
    // Emergency fallback (for debugging only)
    EMERGENCY_FALLBACK_ROLES
  }
}) 