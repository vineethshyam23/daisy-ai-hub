<template>
  <div class="bg-white/90 backdrop-blur-sm border-b border-orange-100 sticky top-0 z-50">
    <UContainer>
      <div class="flex justify-between items-center h-20">
        <!-- Logo und Titel -->
        <button 
          @click="async () => { 
            try {
              trackButtonClick('Navigate to Home via Logo', { 
                currentPage: $route.path,
                userAuthenticated: authStore.isAuthenticated,
                navigationType: 'header_logo'
              }); 
            } catch (error) {
              console.error('Tracking error:', error);
            }
            await router.push('/'); 
          }"
          class="flex items-center space-x-6 group px-4 py-2 transition-all duration-200 cursor-pointer"
        >
          <div class="flex items-center space-x-4">
            <img 
              src="/logo.png" 
              alt="AI Hub Logo"
              class="h-10 w-auto group-hover:scale-105 transition-transform duration-200"
              @error="logoError = true"
            />
            <div v-if="logoError" class="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-200">
              <UIcon name="i-heroicons-cpu-chip" class="w-6 h-6 text-white" />
            </div>
          </div>
          <div class="text-left">
            <div class="flex items-center space-x-2">
              <h1 class="text-xl font-semibold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent group-hover:from-orange-600 group-hover:to-amber-600 transition-all duration-200">
                DAISY
              </h1>
              <span v-if="isDevelopmentEnvironment" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-semibold bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-sm">
                DEV
              </span>
            </div>
            <p class="text-sm text-gray-500 font-light group-hover:text-gray-700 transition-colors duration-200">Intelligent Assistants for Your Work</p>
          </div>
        </button>

        <!-- Navigation & Login -->
        <div class="flex items-center space-x-4">
          <!-- Back to Hub Button (only show if not on index page) -->
          <UButton
            v-if="$route.path !== '/'"
            @click="async () => { 
              try {
                trackButtonClick('Back to AI Hub', { 
                  currentPage: $route.path,
                  userAuthenticated: authStore.isAuthenticated,
                  navigationType: 'back_button'
                }); 
              } catch (error) {
                console.error('Tracking error:', error);
              }
              await router.push('/'); 
            }"
            variant="ghost"
            icon="i-heroicons-arrow-left"
            class="text-gray-600 hover:text-gray-900 cursor-pointer"
            size="lg"
          >
            <span class="hidden sm:inline">Back to Hub</span>
          </UButton>

          <!-- Login/User Section -->
          <div class="flex items-center">
            <UButton
              v-if="!authStore.isAuthenticated"
              @click="async () => { 
                try {
                  trackButtonClick('Navigate to Sign In', { 
                    currentPage: $route.path,
                    navigationType: 'header_signin'
                  }); 
                } catch (error) {
                  console.error('Tracking error:', error);
                }
                await router.push('/login'); 
              }"
              class="bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg hover:from-orange-600 hover:to-amber-600 hover:shadow-xl transition-all font-medium cursor-pointer"
              icon="i-heroicons-user"
              size="lg"
            >
              Sign In
            </UButton>
            
            <!-- User Menu -->
            <div v-else class="flex items-center space-x-4">
              <div class="text-sm font-semibold text-gray-900 truncate max-w-[280px] hidden sm:flex items-center space-x-2">
                <button 
                  @click="async () => { 
                    try {
                      trackButtonClick('Navigate to Profile', { 
                        currentPage: $route.path,
                        userEmail: authStore.userEmail?.split('@')[1] || 'unknown',
                        currentTokens: tokenStore.tokens,
                        navigationType: 'header_profile'
                      }); 
                    } catch (error) {
                      console.error('Tracking error:', error);
                    }
                    await router.push('/profile'); 
                  }"
                  class="flex items-center space-x-2 hover:text-blue-600 transition-colors cursor-pointer underline-offset-2 hover:underline"
                >
                  <UIcon name="i-heroicons-user-circle" class="w-5 h-5 text-gray-600 hover:text-blue-600 transition-colors" />
                  <span>{{ authStore.userEmail }}</span>
                </button>
                <!-- Token display with loading state -->
                <div v-if="tokenStore.isTokenDataReady" :class="['inline-flex items-center px-2 py-1 rounded-full text-xs font-medium', tokenBoxColorClass]">
                  <UIcon name="i-heroicons-currency-dollar" class="w-3 h-3 mr-1" :class="tokenColorClass" />
                  {{ tokens }}
                </div>
                <div v-else-if="tokenStore.isLoading" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
                  <UIcon name="i-heroicons-arrow-path" class="w-3 h-3 animate-spin" />
                </div>
                <div v-else class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200">
                  <UIcon name="i-heroicons-currency-dollar" class="w-3 h-3 mr-1" />
                  --
                </div>
              </div>
              <UButton
                @click="() => authStore.logout()"
                class="bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg hover:from-orange-600 hover:to-amber-600 hover:shadow-xl transition-all font-medium cursor-pointer"
                size="lg"
                icon="i-heroicons-arrow-right-on-rectangle"
              >
                <span class="hidden sm:inline">Sign Out</span>
              </UButton>
            </div>
          </div>
        </div>
      </div>
    </UContainer>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useAdobeTracking } from '~/composables/useAdobeTracking'
import { getApiEnvironment } from '~/config/api.config'

// State
const logoError = ref(false)
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const router = useRouter()

// Adobe Tracking
const { trackButtonClick } = useAdobeTracking()

// Initialize token store
onMounted(async () => {
  // Initialize token store if user is authenticated
  if (authStore.isAuthenticated && authStore.user && !tokenStore.isInitialized) {
    try {
      await tokenStore.init()
    } catch (error) {
      console.error('AIHeader: Error initializing token store:', error)
    }
  }
})

// Watch for auth changes and init tokens
watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
  if (isAuthenticated && authStore.user && !tokenStore.isInitialized) {
    try {
      await tokenStore.init()
    } catch (error) {
      console.error('AIHeader: Error initializing token store after auth change:', error)
    }
  }
})

// Computed values from token store
const tokens = computed(() => tokenStore.tokens)

// Environment detection
const isDevelopmentEnvironment = computed(() => {
  return getApiEnvironment() === 'development'
})

// Color class for token icon based on token count
const tokenColorClass = computed(() => {
  const color = tokenStore.tokensColor
  if (color === 'green') return 'text-green-500'
  if (color === 'yellow') return 'text-yellow-500'
  return 'text-red-500'
})

// Color class for token box based on token count
const tokenBoxColorClass = computed(() => {
  const color = tokenStore.tokensColor
  if (color === 'green') return 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border border-green-200'
  if (color === 'yellow') return 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800 border border-yellow-200'
  return 'bg-gradient-to-r from-red-100 to-rose-100 text-red-800 border border-red-200'
})
</script> 