import { defineStore } from 'pinia'
import { doc, getDoc, setDoc, updateDoc, serverTimestamp } from 'firebase/firestore'
import { useAuthStore } from './auth'

interface UserTokenData {
  tokens: number
  lastResetDate: string
  totalUsage: number
  allTimeUsage: number
  dailyLimit: number
  createdAt: any
  updatedAt: any
}

type ToolName = 'email-responder' | 'social-media-generator' | 'image-generator' | 'meeting-summarizer' | 'approved-metro-tools' | 'document-processor' | 'invoice-validator-sco' | 'multi-document-analyzer' | 'learning-path-creator'

export const useTokenStore = defineStore('tokens', () => {
  const db = useFirestore()
  const authStore = useAuthStore()
  
  // State
  const tokens = ref(0) // Start with 0, will be loaded from Firestore
  const isLoading = ref(false)
  const lastResetDate = ref('')
  const totalUsage = ref(0)
  const allTimeUsage = ref(0)
  const isInitialized = ref(false)
  const dailyLimit = ref(0) // Start with 0, will be loaded from Firestore

  // Constants
  const TOKEN_COSTS: Record<ToolName, number> = {
    'email-responder': 1,
    'social-media-generator': 1,
    'image-generator': 2,
    'meeting-summarizer': 1,
    'approved-metro-tools': 0,
    'document-processor': 1,
    'invoice-validator-sco': 0,
    'multi-document-analyzer': 2,
    'learning-path-creator': 1
  }

  // Computed
  const canUseTokens = computed(() => tokens.value > 0)
  const tokensPercentage = computed(() => Math.max(0, (tokens.value / dailyLimit.value) * 100))
  const tokensColor = computed(() => {
    const percentage = tokensPercentage.value
    if (percentage > 60) return 'green'
    if (percentage > 20) return 'yellow'
    return 'red'
  })
  const isTokenDataReady = computed(() => isInitialized.value && !isLoading.value && dailyLimit.value > 0)

  // Helper functions
  const getTodayDateString = () => {
    return new Date().toISOString().split('T')[0]
  }

  const shouldResetTokens = (lastReset: string) => {
    const today = getTodayDateString()
    return lastReset !== today
  }

  // Get role-based token limit
  const getRoleBasedTokenLimit = async (): Promise<number> => {
    try {
      const { useRoleStore } = await import('./roles')
      const roleStore = useRoleStore()
      
      if (!roleStore.isInitialized) {
        await roleStore.init()
      }
      
      return roleStore.dailyTokenLimit || 50
    } catch (error) {
      console.error('Error getting role-based token limit:', error)
      return 50
    }
  }

  // Initialize user tokens in Firestore
  const initializeUserTokens = async (): Promise<UserTokenData> => {
    if (!authStore.user?.uid) {
      throw new Error('User not authenticated')
    }

    const today = getTodayDateString()
    const roleBasedLimit = await getRoleBasedTokenLimit()
    
    const initialData: UserTokenData = {
      tokens: roleBasedLimit,
      lastResetDate: today,
      totalUsage: 0,
      allTimeUsage: 0,
      dailyLimit: roleBasedLimit,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp()
    }

    try {
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      await setDoc(userRef, initialData)
      return {
        ...initialData,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    } catch (error) {
      console.error('Error initializing user tokens:', error)
      throw error
    }
  }

  // Load user token data from Firestore
  const loadUserTokens = async () => {
    if (!authStore.user?.uid) {
      console.warn('Cannot load tokens: User not authenticated')
      return
    }

    // Only set loading if not already loading (to avoid conflicts with init)
    const wasLoading = isLoading.value
    if (!wasLoading) {
      isLoading.value = true
    }
    
    try {
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      const docSnap = await getDoc(userRef)
      
      let userData: UserTokenData
      
      if (!docSnap.exists()) {
        // Create new user token document
        userData = await initializeUserTokens()
      } else {
        userData = docSnap.data() as UserTokenData
        
        // Check if tokens need daily reset
        if (shouldResetTokens(userData.lastResetDate)) {
          await resetDailyTokens()
          return // resetDailyTokens will reload the data
        }
        
        // Check if daily limit needs to be updated based on current role
        const currentRoleLimit = await getRoleBasedTokenLimit()
        if (userData.dailyLimit !== currentRoleLimit) {
          await updateTokenLimit(currentRoleLimit)
          return // updateTokenLimit will reload the data
        }
      }
      
      // Update local state
      tokens.value = userData.tokens
      lastResetDate.value = userData.lastResetDate
      totalUsage.value = userData.totalUsage || 0
      allTimeUsage.value = userData.allTimeUsage || 0
      dailyLimit.value = userData.dailyLimit || 50
      isInitialized.value = true
            
    } catch (error) {
      console.error('Error loading user tokens:', error)
      // Fallback initialization - preserve existing allTimeUsage if possible
      const roleBasedLimit = await getRoleBasedTokenLimit()
      tokens.value = roleBasedLimit
      dailyLimit.value = roleBasedLimit
      lastResetDate.value = getTodayDateString()
      totalUsage.value = 0
      // Only reset allTimeUsage if it's currently 0 (first time user)
      if (allTimeUsage.value === 0) {
        allTimeUsage.value = 0
      }
      isInitialized.value = true
    } finally {
      if (!wasLoading) {
        isLoading.value = false
      }
    }
  }

  // Reset daily tokens
  const resetDailyTokens = async () => {
    if (!authStore.user?.uid) return

    try {
      const today = getTodayDateString()
      const roleBasedLimit = await getRoleBasedTokenLimit()
      
      // First, get the current data to preserve allTimeUsage
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      const currentDoc = await getDoc(userRef)
      const currentData = currentDoc.exists() ? currentDoc.data() as UserTokenData : null
      
      // Preserve the existing allTimeUsage, or default to current local value
      const preservedAllTimeUsage = currentData?.allTimeUsage ?? allTimeUsage.value ?? 0
      
      const userData: UserTokenData = {
        tokens: roleBasedLimit,
        lastResetDate: today,
        totalUsage: 0, // Reset daily usage
        allTimeUsage: preservedAllTimeUsage, // Always preserve all-time usage
        dailyLimit: roleBasedLimit,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp()
      }

      await updateDoc(userRef, {
        tokens: userData.tokens,
        lastResetDate: userData.lastResetDate,
        totalUsage: userData.totalUsage,
        allTimeUsage: userData.allTimeUsage,
        dailyLimit: userData.dailyLimit,
        updatedAt: userData.updatedAt
      })
      
      // Update local state
      tokens.value = roleBasedLimit
      lastResetDate.value = today
      totalUsage.value = 0
      allTimeUsage.value = preservedAllTimeUsage // Ensure allTimeUsage is never reset
      dailyLimit.value = roleBasedLimit
      
    } catch (error) {
      console.error('Error resetting daily tokens:', error)
    }
  }

  // Update token limit based on role change
  const updateTokenLimit = async (newLimit: number) => {
    if (!authStore.user?.uid) return

    try {
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      
      // If user gets more tokens, give them the difference
      // If they get fewer tokens, don't reduce current tokens until next reset
      const newTokens = Math.max(tokens.value, newLimit)
      
      await updateDoc(userRef, {
        dailyLimit: newLimit,
        tokens: newTokens,
        updatedAt: serverTimestamp()
      })
      
      // Update local state
      tokens.value = newTokens
      dailyLimit.value = newLimit
      
    } catch (error) {
      console.error('Error updating token limit:', error)
    }
  }

  // Check if user has sufficient tokens for an assistant
  const hasTokensForAssistant = (assistantName: string): boolean => {
    const cost = TOKEN_COSTS[assistantName as ToolName] || 1
    return tokens.value >= cost
  }

  // Consume tokens for a specific tool
  const consumeTokens = async (toolName: string): Promise<boolean> => {
    if (!authStore.user?.uid) {
      throw new Error('User not authenticated')
    }

    const cost = TOKEN_COSTS[toolName as ToolName] || 1
    
    if (tokens.value < cost) {
      return false
    }

    try {
      const newTokenCount = Math.max(0, tokens.value - cost)
      const newTotalUsage = totalUsage.value + cost
      const newAllTimeUsage = allTimeUsage.value + cost
      
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      await updateDoc(userRef, {
        tokens: newTokenCount,
        totalUsage: newTotalUsage,
        allTimeUsage: newAllTimeUsage,
        updatedAt: serverTimestamp()
      })
      
      // Update local state
      tokens.value = newTokenCount
      totalUsage.value = newTotalUsage
      allTimeUsage.value = newAllTimeUsage
      
      return true
    } catch (error) {
      console.error('Error consuming tokens:', error)
      return false
    }
  }

  // Use specific amount of tokens (for dynamic costs)
  const useTokens = async (amount: number): Promise<boolean> => {
    if (!authStore.user?.uid) {
      throw new Error('User not authenticated')
    }

    if (tokens.value < amount) {
      return false
    }

    try {
      const newTokenCount = Math.max(0, tokens.value - amount)
      const newTotalUsage = totalUsage.value + amount
      const newAllTimeUsage = allTimeUsage.value + amount
      
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      await updateDoc(userRef, {
        tokens: newTokenCount,
        totalUsage: newTotalUsage,
        allTimeUsage: newAllTimeUsage,
        updatedAt: serverTimestamp()
      })
      
      // Update local state
      tokens.value = newTokenCount
      totalUsage.value = newTotalUsage
      allTimeUsage.value = newAllTimeUsage
      
      return true
    } catch (error) {
      console.error('Error using tokens:', error)
      return false
    }
  }

  // Add tokens (for token codes, admin grants, etc.)
  const addTokens = async (amount: number): Promise<boolean> => {
    if (!authStore.user?.uid) {
      throw new Error('User not authenticated')
    }

    try {
      const newTokenCount = Math.min(tokens.value + amount, dailyLimit.value)
      const actualAdded = newTokenCount - tokens.value
      
      if (actualAdded <= 0) {
        return false // Already at limit
      }
      
      const userRef = doc(db, 'userTokens', authStore.user.uid)
      await updateDoc(userRef, {
        tokens: newTokenCount,
        updatedAt: serverTimestamp()
      })
      
      // Update local state
      tokens.value = newTokenCount

      return true
    } catch (error) {
      console.error('Error adding tokens:', error)
      return false
    }
  }

  // Get token cost for specific tool
  const getTokenCost = (toolName: string): number => {
    return TOKEN_COSTS[toolName as ToolName] || 1
  }

  // Get hours until next reset
  const getHoursUntilReset = (): number => {
    const now = new Date()
    const tomorrow = new Date(now)
    tomorrow.setDate(tomorrow.getDate() + 1)
    tomorrow.setHours(0, 0, 0, 0)
    
    const diff = tomorrow.getTime() - now.getTime()
    return Math.ceil(diff / (1000 * 60 * 60))
  }

  // Update tokens based on current role (for role changes)
  const updateTokensForRole = async () => {
    if (!authStore.user?.uid) return
    
    try {
      const roleBasedLimit = await getRoleBasedTokenLimit()
      
      // If daily limit is different, update it
      if (dailyLimit.value !== roleBasedLimit) {
        await updateTokenLimit(roleBasedLimit)
      }
      
      // If it's a new day, reset tokens
      if (shouldResetTokens(lastResetDate.value)) {
        await resetDailyTokens()
      }
    } catch (error) {
      console.error('Error updating tokens for role:', error)
    }
  }

  // Initialize token store
  const init = async () => {
    if (isInitialized.value || !authStore.isAuthenticated) {
      return
    }
    
    isLoading.value = true
    
    try {
      await loadUserTokens()
    } catch (error) {
      console.error('Error initializing token store:', error)
      // Set fallback values on error
      const roleBasedLimit = await getRoleBasedTokenLimit()
      tokens.value = roleBasedLimit
      dailyLimit.value = roleBasedLimit
      lastResetDate.value = getTodayDateString()
      totalUsage.value = 0
      allTimeUsage.value = 0
      isInitialized.value = true
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    tokens: readonly(tokens),
    isLoading: readonly(isLoading),
    lastResetDate: readonly(lastResetDate),
    totalUsage: readonly(totalUsage),
    allTimeUsage: readonly(allTimeUsage),
    isInitialized: readonly(isInitialized),
    dailyLimit: readonly(dailyLimit),
    
    // Constants
    TOKEN_COSTS,
    
    // Computed
    canUseTokens,
    tokensPercentage,
    tokensColor,
    isTokenDataReady,
    
    // Methods
    init,
    loadUserTokens,
    hasTokensForAssistant,
    consumeTokens,
    useTokens,
    addTokens,
    getTokenCost,
    getHoursUntilReset,
    resetDailyTokens,
    updateTokensForRole,
    updateTokenLimit
  }
}) 