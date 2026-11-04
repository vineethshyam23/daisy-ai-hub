<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50">
      <!-- Unified Header -->
      <AIHeader />

      <!-- Main Content -->
      <UContainer class="py-8">
        <!-- Intro Section -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
          <div class="flex items-center space-x-4 mb-6">
            <div class="flex-shrink-0 w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
              <UIcon name="i-heroicons-home" class="w-6 h-6 text-white" />
            </div>
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900 mb-1">Welcome</h1>
              <p class="text-gray-600">Find information about getting started, onboarding processes, and welcome resources.</p>
            </div>
          </div>
          <!-- Search Widget Container -->
          <div class="relative">
            <input 
              id="welcomeSearchTrigger"
              type="text" 
              :placeholder="isWidgetReady ? 'Search welcome guides, onboarding, and getting started...' : 'Loading search widget...'"
              :disabled="!isWidgetReady"
              :class="[
                'w-full pl-4 pr-12 py-4 border rounded-lg text-lg transition-all duration-200',
                isWidgetReady 
                  ? 'border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 cursor-pointer hover:border-gray-400' 
                  : 'border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed'
              ]"
              @click="activateWidget"
            />
            
            <!-- Loading indicator -->
            <div v-if="!isWidgetReady" class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-orange-500"></div>
            </div>
            
            <!-- Ready indicator -->
            <div v-else class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <UIcon name="i-heroicons-magnifying-glass" class="w-5 h-5 text-gray-400" />
            </div>
          </div>
        </div>

        <!-- Disclaimer -->
        <DisclaimerBox 
          disclaimer-text="AI does its best, but it's not flawless—check the sources we provide to make sure everything adds up."
          class="mb-6"
        />
      </UContainer>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAIHubStore } from '~/stores/aiHub'
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useRoleStore } from '~/stores/roles'

// Stores
const aiHub = useAIHubStore()
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const roleStore = useRoleStore()

// Widget management
const currentWidget = ref(null)
const isWidgetReady = ref(false)

// Fast Welcome Search Widget loading using global script manager
const loadWelcomeWidget = () => {
  
  // Clear any existing widgets
  currentWidget.value = null
  isWidgetReady.value = false
  
  // Clean up any existing widgets
  const existingWidgets = document.querySelectorAll('gen-search-widget')
  existingWidgets.forEach(widget => widget.remove())
  
  // Use global script manager
  window.onGoogleSearchReady(() => {
    
    // Create widget immediately
    const widget = document.createElement('gen-search-widget')
    widget.setAttribute('configId', '72235cf3-7873-4821-9f41-7bf4b8e862af')
    widget.setAttribute('location', 'eu')
    widget.setAttribute('triggerId', 'welcomeSearchTrigger')
    widget.setAttribute('anchorsTarget', '_blank')
    widget.setAttribute('placeholder', 'Search welcome guides, onboarding, and getting started...')
    
    // Add event listeners
    widget.addEventListener('load', () => {
      isWidgetReady.value = true
    })
    
    widget.addEventListener('error', (event) => {
      console.error('❌ Welcome Widget error:', event)
      isWidgetReady.value = false
    })
    
    // Add to page
    document.body.appendChild(widget)
    currentWidget.value = widget
    
    // If script is already loaded, show ready immediately
    if (window.__googleSearchReady) {
      isWidgetReady.value = true
    } else {
      // Otherwise set as ready after short delay
      setTimeout(() => {
        isWidgetReady.value = true
      }, 100)
    }
  })
}

// Simple cleanup
const cleanup = () => {
  if (currentWidget.value) {
    currentWidget.value.remove()
    currentWidget.value = null
  }
  isWidgetReady.value = false
}

// Instant widget activation
const activateWidget = () => {
  if (!isWidgetReady.value) return
  
  // Force activate the widget
  if (currentWidget.value && currentWidget.value.shadowRoot) {
    const internalTrigger = currentWidget.value.shadowRoot.querySelector('input')
    if (internalTrigger) {
      internalTrigger.click()
      internalTrigger.focus()
    } 
  }
}

// Initialize stores after navigation (auth is handled by middleware)
onMounted(async () => {
  // Initialize other stores
  try {
    if (!roleStore.isInitialized) await roleStore.init()
    if (!tokenStore.isInitialized) await tokenStore.init()
    if (!aiHub.isOrderLoaded) await aiHub.init()
  } catch (error) {
    console.error('Error initializing stores:', error)
  }

  // Load the widget (now synchronous)
  loadWelcomeWidget()
})

// Cleanup on unmount and route change
onBeforeUnmount(() => {
  cleanup()
})

// Also cleanup when navigating away
onBeforeRouteLeave(() => {
  cleanup()
})

// SEO
useHead({
  title: 'Welcome Search - DAISY',
  meta: [
    { name: 'description', content: 'Search for welcome information, onboarding guides, and getting started resources.' }
  ]
})
</script> 