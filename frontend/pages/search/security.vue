<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50">
      <!-- Unified Header -->
      <AIHeader />

      <!-- Main Content -->
      <UContainer class="py-8">
        <!-- Intro Section -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
          <div class="flex items-center space-x-4 mb-6">
            <div class="flex-shrink-0 w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center">
              <UIcon name="i-heroicons-shield-check" class="w-6 h-6 text-white" />
            </div>
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900 mb-1">Information Security Resources</h1>
              <p class="text-gray-600">Find security policies, guidelines, and best practices for protecting data and systems.</p>
            </div>
          </div>
          
          <!-- Search Widget Container -->
          <div class="relative">
            <input 
              id="securitySearchTrigger"
              type="text" 
              :placeholder="isWidgetReady ? 'Search security policies, guidelines, best practices...' : 'Loading search widget...'"
              :disabled="!isWidgetReady"
              :class="[
                'w-full pl-4 pr-12 py-4 border rounded-lg text-lg transition-all duration-200',
                isWidgetReady 
                  ? 'border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 cursor-pointer hover:border-gray-400' 
                  : 'border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed'
              ]"
              @click="activateWidget"
            />
            
            <!-- Loading indicator -->
            <div v-if="!isWidgetReady" class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-emerald-500"></div>
            </div>
            
            <!-- Ready indicator -->
            <div v-else class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <UIcon name="i-heroicons-magnifying-glass" class="w-5 h-5 text-gray-400" />
            </div>
          </div>
        </div>

        <!-- Disclaimer -->
        <DisclaimerBox 
          disclaimer-text="AI does its best, but it's not flawless—check the sources we provide to make sure everything adds up and reach out to the Information Security Team in case of questions or concerns."
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

// Fast Security Search Widget loading using global script manager
const loadSecurityWidget = () => {
  
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
    widget.setAttribute('configId', '6d2cc589-f8c5-4fa0-b340-d9cb9cf1843c')
    widget.setAttribute('location', 'eu')
    widget.setAttribute('triggerId', 'securitySearchTrigger')
    widget.setAttribute('anchorsTarget', '_blank')
    widget.setAttribute('placeholder', 'Search security policies, guidelines, best practices...')
    
    // Add event listeners
    widget.addEventListener('load', () => {
      isWidgetReady.value = true
    })
    
    widget.addEventListener('error', (event) => {
      console.error('❌ Security Widget error:', event)
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
  loadSecurityWidget()
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
  title: 'Information Security Search - DAISY',
  meta: [
    { name: 'description', content: 'Search information security policies and guidelines.' }
  ]
})
</script>

