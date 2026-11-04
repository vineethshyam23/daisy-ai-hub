<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gray-800 rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        DAISY
      </h2>
      <p class="text-gray-600 font-light">Loading Profile...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-gray-800 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gray-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Full-Width Header Banner -->
    <div class="relative bg-gradient-to-r from-gray-800 via-gray-600 to-gray-500 border-b border-gray-700 overflow-hidden">
      <!-- Background Patterns -->
      <div class="absolute inset-0 opacity-10">
        <!-- User Profile Patterns -->
        <div class="absolute top-4 right-8 w-16 h-16 border-2 border-white rounded-full"></div>
        <div class="absolute top-12 right-32 w-8 h-8 border border-white rounded-full"></div>
        <div class="absolute top-20 right-16 w-4 h-4 bg-white rounded-full"></div>
        
        <!-- Settings Grid -->
        <div class="absolute top-8 right-48 w-12 h-12 border border-white rounded-lg"></div>
        <div class="absolute top-24 right-56 w-6 h-6 border border-white rounded"></div>
        <div class="absolute top-16 right-72 w-8 h-8 border border-white rounded-lg"></div>
        
        <!-- Account Management Icons -->
        <div class="absolute top-32 right-12 w-10 h-10 border border-white rounded-lg"></div>
        <div class="absolute top-40 right-40 w-6 h-6 bg-white rounded"></div>
        <div class="absolute top-44 right-64 w-4 h-4 border border-white rounded-full"></div>
        
        <!-- Network Pattern -->
        <div class="absolute top-6 right-20 w-px h-8 bg-white opacity-30"></div>
        <div class="absolute top-14 right-28 w-6 h-px bg-white opacity-30"></div>
        <div class="absolute top-22 right-44 w-px h-12 bg-white opacity-30"></div>
        <div class="absolute top-36 right-24 w-8 h-px bg-white opacity-30"></div>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-gray-500 rounded-xl flex items-center justify-center mr-6 border border-gray-400">
              <UIcon name="i-heroicons-user-circle" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">
                User Profile
              </h1>
              <p class="text-lg text-gray-100 font-light">Manage your account and token usage</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>

    <UContainer class="py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Profile Information -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-8">
          <div class="flex items-center space-x-2 mb-6">
            <UIcon name="i-heroicons-identification" class="text-2xl text-gray-800" />
            <h2 class="text-2xl font-bold text-gray-900">Account Information</h2>
          </div>
          
          <div class="space-y-6">
            <!-- Email -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-2">
                <UIcon name="i-heroicons-envelope" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">Email Address</label>
              </div>
              <p class="text-lg font-semibold text-gray-900">{{ authStore.user?.email || 'Not available' }}</p>
            </div>

            <!-- User ID -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-2">
                <UIcon name="i-heroicons-key" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">User ID</label>
              </div>
              <p class="text-sm font-mono text-gray-600 break-all">{{ authStore.user?.uid || 'Not available' }}</p>
            </div>

            <!-- Account Created -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-2">
                <UIcon name="i-heroicons-calendar-days" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">Member Since</label>
              </div>
              <p class="text-lg text-gray-900">{{ formatDate(authStore.user?.metadata?.creationTime) }}</p>
            </div>

            <!-- Current Role Information -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-4">
                <UIcon name="i-heroicons-shield-check" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">Current Role</label>
              </div>
              
              <div class="flex items-center justify-between mb-4">
                <div>
                  <div class="text-lg font-semibold text-gray-900">
                    {{ roleStore.rolePermissions?.displayName || 'Loading...' }}
                  </div>
                  <div class="text-sm text-gray-600">
                    {{ roleStore.rolePermissions?.description || 'Loading role information...' }}
                  </div>
                </div>
                <div class="flex flex-col items-end space-y-2">
                  <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
                    {{ roleStore.dailyTokenLimit }} tokens/day
                  </span>
                  <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">
                    {{ roleStore.rolePermissions?.allowedAssistants?.length || 0 }} assistants
                  </span>
                </div>
              </div>
              
              <!-- Admin Panel Link -->
              <div v-if="roleStore.isAdmin" class="pt-4 border-t border-gray-200">
                <NuxtLink
                  to="/admin/users"
                  @click="trackButtonClick('Navigate to Admin Panel', { 
                    userRole: roleStore.rolePermissions?.displayName || 'unknown',
                    fromPage: 'profile'
                  })"
                  class="inline-flex items-center px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md"
                >
                  <UIcon name="i-heroicons-users" class="w-4 h-4 mr-2" />
                  Manage Users & Roles
                </NuxtLink>
                <p class="text-xs text-gray-500 mt-2">
                  Administrator access to user and role management
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Token Management -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-8">
          <div class="flex items-center space-x-2 mb-6">
            <UIcon name="i-heroicons-currency-dollar" class="text-2xl text-gray-800" />
            <h2 class="text-2xl font-bold text-gray-900">Token Management</h2>
          </div>
          
          <div class="space-y-6">
            <!-- Current Tokens -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <UIcon name="i-heroicons-currency-dollar" class="text-gray-600" />
                  <label class="text-sm font-medium text-gray-700">Current Tokens</label>
                </div>
                <div v-if="tokenStore.isTokenDataReady" class="flex items-center space-x-2">
                  <div :class="[
                    'w-3 h-3 rounded-full',
                    tokenStore.tokensColor === 'green' ? 'bg-green-500' :
                    tokenStore.tokensColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                  ]"></div>
                  <span :class="[
                    'text-xs font-medium',
                    tokenStore.tokensColor === 'green' ? 'text-green-600' :
                    tokenStore.tokensColor === 'yellow' ? 'text-yellow-600' : 'text-red-600'
                  ]">
                    {{ tokenStore.tokensPercentage.toFixed(0) }}%
                  </span>
                </div>
                <div v-else class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full bg-gray-300 animate-pulse"></div>
                  <span class="text-xs font-medium text-gray-400">Loading...</span>
                </div>
              </div>
              
              <div v-if="tokenStore.isTokenDataReady" class="flex items-center justify-between mb-3">
                <span class="text-3xl font-bold text-gray-900">{{ tokenStore.tokens }}</span>
                <span class="text-sm text-gray-500">remaining</span>
              </div>
              <div v-else class="flex items-center justify-between mb-3">
                <div class="w-16 h-8 bg-gray-200 rounded animate-pulse"></div>
                <span class="text-sm text-gray-400">loading...</span>
              </div>
              
              <!-- Progress Bar -->
              <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
                <div 
                  v-if="tokenStore.isTokenDataReady"
                  :class="[
                    'h-3 rounded-full transition-all duration-300',
                    tokenStore.tokensColor === 'green' ? 'bg-green-500' :
                    tokenStore.tokensColor === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'
                  ]"
                  :style="`width: ${tokenStore.tokensPercentage}%`"
                ></div>
                <div v-else class="h-3 rounded-full bg-gray-300 animate-pulse w-1/2"></div>
              </div>
              
              <p v-if="tokenStore.isTokenDataReady" class="text-sm text-gray-600">
                Resets in {{ tokenStore.getHoursUntilReset() }} hours
              </p>
              <p v-else class="text-sm text-gray-400">
                Loading reset time...
              </p>
            </div>

            <!-- Usage Statistics -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-4">
                <UIcon name="i-heroicons-chart-bar" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">Usage Statistics</label>
              </div>
              
              <div v-if="tokenStore.isTokenDataReady" class="space-y-4">
                <!-- Today's Usage -->
                <div class="grid grid-cols-2 gap-4">
                  <div class="text-center p-4 bg-white rounded-lg border border-gray-200">
                    <div class="text-2xl font-bold text-gray-900">{{ tokenStore.totalUsage }}</div>
                    <div class="text-xs text-gray-600 font-medium">Today's Usage</div>
                  </div>
                  <div class="text-center p-4 bg-white rounded-lg border border-gray-200">
                    <div class="text-2xl font-bold text-gray-900">{{ tokenStore.tokens }}</div>
                    <div class="text-xs text-gray-600 font-medium">Remaining</div>
                  </div>
                </div>
                
                <!-- All-Time Usage -->
                <div class="text-center p-4 bg-white rounded-lg border border-gray-200">
                  <div class="text-3xl font-bold text-gray-900">{{ tokenStore.allTimeUsage.toLocaleString() }}</div>
                  <div class="text-sm text-gray-700 font-medium flex items-center justify-center space-x-2">
                    <UIcon name="i-heroicons-trophy" class="w-4 h-4" />
                    <span>All-Time Tokens Used</span>
                  </div>
                  <div class="text-xs text-gray-600 mt-1">Since account creation</div>
                </div>
              </div>
              
              <div v-else class="space-y-4">
                <!-- Loading states -->
                <div class="grid grid-cols-2 gap-4">
                  <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <div class="w-12 h-6 bg-gray-200 rounded mx-auto mb-2 animate-pulse"></div>
                    <div class="text-xs text-gray-400">Loading...</div>
                  </div>
                  <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <div class="w-12 h-6 bg-gray-200 rounded mx-auto mb-2 animate-pulse"></div>
                    <div class="text-xs text-gray-400">Loading...</div>
                  </div>
                </div>
                <div class="text-center p-4 bg-gray-50 rounded-lg">
                  <div class="w-20 h-8 bg-gray-200 rounded mx-auto mb-2 animate-pulse"></div>
                  <div class="text-xs text-gray-400">Loading all-time usage...</div>
                </div>
              </div>
            </div>

            <!-- Token Top-up -->
            <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <div class="flex items-center space-x-3 mb-4">
                <UIcon name="i-heroicons-gift" class="text-gray-600" />
                <label class="text-sm font-medium text-gray-700">Redeem Token Code</label>
              </div>
              
              <div class="space-y-4">
                <input
                  v-model="tokenCode"
                  type="text"
                  placeholder="Enter your token code..."
                  class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-gray-400 focus:outline-none transition-colors text-lg font-mono uppercase"
                  :disabled="isRedeeming"
                />
                
                <UButton 
                  @click="redeemTokenCode"
                  :loading="isRedeeming"
                  :disabled="!tokenCode.trim() || isRedeeming"
                  color="primary"
                  size="lg"
                  :class="[
                    'w-full font-semibold shadow-sm hover:shadow-md transform transition-all duration-300',
                    tokenCode.trim() && !isRedeeming
                      ? 'bg-gray-800 hover:bg-gray-900 text-white hover:scale-105 cursor-pointer' 
                      : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  ]"
                  icon="i-heroicons-gift"
                >
                  <span v-if="isRedeeming">Redeeming Code...</span>
                  <span v-else-if="!tokenCode.trim()">Enter Code to Redeem</span>
                  <span v-else>Redeem Code</span>
                </UButton>
                
                <div class="text-xs text-gray-500 text-center">
                  <!--<p>💡 Try code: <code class="bg-gray-100 px-2 py-1 rounded font-mono">data50</code></p>-->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Actions -->
      <div class="mt-8 bg-white border border-gray-200 rounded-xl shadow-sm p-8">
        <div class="flex items-center space-x-2 mb-6">
          <UIcon name="i-heroicons-cog-6-tooth" class="text-2xl text-gray-800" />
          <h2 class="text-2xl font-bold text-gray-900">Account Actions</h2>
        </div>
        
        <div class="flex flex-wrap gap-4">
          <UButton
            @click="refreshTokens"
            variant="outline"
            size="lg"
            class="cursor-pointer px-6 py-3 border border-gray-300 hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 group"
          >
            <UIcon name="i-heroicons-arrow-path" class="w-5 h-5 text-gray-600 group-hover:text-gray-700 mr-2" />
            <span class="text-gray-700 group-hover:text-gray-800 font-medium">Refresh Tokens</span>
          </UButton>
          
          <UButton
            @click="changePassword"
            :loading="isChangingPassword"
            :disabled="isChangingPassword"
            variant="outline"
            size="lg"
            class="cursor-pointer px-6 py-3 border border-blue-300 hover:border-blue-400 hover:bg-blue-50 transition-all duration-200 group"
          >
            <UIcon name="i-heroicons-lock-closed" class="w-5 h-5 text-blue-600 group-hover:text-blue-700 mr-2" />
            <span class="text-blue-700 group-hover:text-blue-800 font-medium">
              {{ isChangingPassword ? 'Sending Email...' : 'Change Password' }}
            </span>
          </UButton>
          
          <UButton
            @click="() => { 
              trackButtonClick('Logout', { 
                userRole: roleStore.rolePermissions?.displayName || 'unknown',
                fromPage: 'profile',
                sessionLength: authStore.user?.metadata?.lastSignInTime ? 
                  Math.round((Date.now() - new Date(authStore.user.metadata.lastSignInTime).getTime()) / 60000) : 
                  'unknown'
              }); 
              authStore.logout(); 
            }"
            variant="outline"
            size="lg"
            class="cursor-pointer px-6 py-3 border border-red-300 hover:border-red-400 hover:bg-red-50 transition-all duration-200 group"
          >
            <UIcon name="i-heroicons-arrow-left-on-rectangle" class="w-5 h-5 text-red-600 group-hover:text-red-700 mr-2" />
            <span class="text-red-700 group-hover:text-red-800 font-medium">Logout</span>
          </UButton>
        </div>
      </div>
    </UContainer>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useRoleStore } from '~/stores/roles'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Stores
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const roleStore = useRoleStore()

// Adobe Tracking
const { trackButtonClick, trackError } = useAdobeTracking()

// State
const tokenCode = ref('')
const isRedeeming = ref(false)
const isChangingPassword = ref(false)

// Valid token codes and their rewards
const TOKEN_CODES = {
  'DATA50': 50,
  'data50': 50,
  'WELCOME': 25,
  'welcome': 25
}

// Client-side auth check and redirect
onMounted(async () => {
  try {
    // Wait for auth store to be initialized
    if (!authStore.isInitialized) {
      await authStore.init()
    }
    
    // Redirect to login if not authenticated
    if (!authStore.isAuthenticated) {
      await navigateTo('/login')
      return
    }

    // Initialize role store
    if (!roleStore.isInitialized) {
      try {
        await roleStore.init()
      } catch (error) {
        console.error('Profile: Error initializing role store:', error)
        
        // Track role store initialization error
        trackError('profile_role_init_failed', 'Failed to initialize role store on profile page', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user
        })
      }
    }

    // Initialize token store
    if (!tokenStore.isInitialized) {
      try {
        await tokenStore.init()
      } catch (error) {
        console.error('Profile: Error initializing token store:', error)
        
        // Track token store initialization error
        trackError('profile_token_init_failed', 'Failed to initialize token store on profile page', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user
        })
      }
    }
  } catch (error) {
    console.error('Profile: Error in onMounted:', error)
    
    // Track general profile initialization error
    trackError('profile_init_failed', 'Critical error during profile page initialization', {
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      isAuthenticated: authStore.isAuthenticated,
      hasUser: !!authStore.user,
      authInitialized: authStore.isInitialized
    })
  }
})

// Watch for auth state changes
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    navigateTo('/login')
  }
})

// Methods
const formatDate = (timestamp) => {
  if (!timestamp) return 'Unknown'
  try {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (error) {
    return 'Unknown'
  }
}

const refreshTokens = async () => {
  try {
    // Track refresh action
    trackButtonClick('Refresh Tokens', {
      currentTokens: tokenStore.tokens,
      userRole: roleStore.rolePermissions?.displayName || 'unknown',
      fromPage: 'profile'
    })
    
    await tokenStore.loadUserTokens()
    await tokenStore.updateTokensForRole()
    const toast = useToast()
    toast.add({
      title: 'Tokens Refreshed',
      description: 'Your token information has been updated from Firestore.',
      color: 'green'
    })
  } catch (error) {
    // Track token refresh error
    trackError('profile_token_refresh_failed', 'Failed to refresh user token information', {
      currentTokens: tokenStore.tokens,
      userRole: roleStore.rolePermissions?.displayName || 'unknown',
      userId: authStore.user?.uid || 'unknown',
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      isTokenStoreInitialized: tokenStore.isInitialized,
      operation: 'refresh_tokens'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Refresh Failed',
      description: 'Failed to refresh tokens. Please try again.',
      color: 'red'
    })
  }
}

const redeemTokenCode = async () => {
  if (!tokenCode.value.trim()) return
  
  // Track redemption attempt
  trackButtonClick('Redeem Token Code', {
    codeLength: tokenCode.value.trim().length,
    currentTokens: tokenStore.tokens,
    userRole: roleStore.rolePermissions?.displayName || 'unknown'
  })
  
  isRedeeming.value = true
  
  try {
    const code = tokenCode.value.trim().toUpperCase()
    const reward = TOKEN_CODES[code] || TOKEN_CODES[tokenCode.value.trim()]
    
    if (!reward) {
      const toast = useToast()
      toast.add({
        title: 'Invalid Code',
        description: 'The code you entered is not valid. Please check and try again.',
        color: 'red'
      })
      return
    }

    // Try to add tokens using the new Firestore-based system
    const success = await tokenStore.addTokens(reward)
    
    if (!success) {
      const toast = useToast()
      toast.add({
        title: 'Already at Maximum',
        description: 'You already have the maximum number of tokens for today.',
        color: 'orange'
      })
      return
    }
    
    const toast = useToast()
    toast.add({
      title: 'Code Redeemed!',
      description: `Successfully added tokens to your account.`,
      color: 'green'
    })
    
    tokenCode.value = ''
    
  } catch (error) {
    console.error('Token redemption error:', error)
    
    // Track token redemption error
    trackError('profile_token_redemption_failed', 'Failed to redeem token code', {
      codeLength: tokenCode.value.trim().length,
      currentTokens: tokenStore.tokens,
      userRole: roleStore.rolePermissions?.displayName || 'unknown',
      userId: authStore.user?.uid || 'unknown',
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      operation: 'redeem_token_code',
      codeWasValid: !!TOKEN_CODES[tokenCode.value.trim().toUpperCase()]
    })
    
    const toast = useToast()
    toast.add({
      title: 'Redemption Failed',
      description: 'Failed to redeem code. Please try again.',
      color: 'red'
    })
  } finally {
    isRedeeming.value = false
  }
}

const changePassword = async () => {
  // Track password change attempt
  trackButtonClick('Change Password', {
    userRole: roleStore.rolePermissions?.displayName || 'unknown',
    fromPage: 'profile',
    userEmail: authStore.user?.email || 'unknown',
    accountAge: authStore.user?.metadata?.creationTime ? 
      Math.round((Date.now() - new Date(authStore.user.metadata.creationTime).getTime()) / (1000 * 60 * 60 * 24)) : 
      'unknown'
  })
  
  isChangingPassword.value = true
  
  try {
    const result = await authStore.changePassword()
    
    if (result.success) {
      const toast = useToast()
      toast.add({
        title: 'Password Change Email Sent',
        description: result.message,
        color: 'green'
      })
    }
    
  } catch (error) {
    console.error('Password change error:', error)
    
    // Track password change error
    trackError('profile_password_change_failed', 'Failed to send password change email', {
      userRole: roleStore.rolePermissions?.displayName || 'unknown',
      userId: authStore.user?.uid || 'unknown',
      userEmail: authStore.user?.email || 'unknown',
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      operation: 'change_password'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Password Change Failed',
      description: authStore.error || 'Failed to send password change email. Please try again.',
      color: 'red'
    })
  } finally {
    isChangingPassword.value = false
  }
}

// SEO
useHead({
  title: 'Profile - DAISY',
  meta: [
    { name: 'description', content: 'Manage your account settings and token usage on DAISY.' }
  ]
})
</script> 