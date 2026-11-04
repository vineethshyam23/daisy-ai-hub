<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-blue-50 via-blue-25 to-indigo-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
      <h2 class="text-2xl font-bold bg-gradient-to-r from-blue-500 to-indigo-500 bg-clip-text text-transparent mb-2">
        AI Hub
      </h2>
      <p class="text-gray-600 font-light">Loading Approved External Tools...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-blue-50 via-blue-25 to-indigo-50">
    <!-- Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-blue-800 via-blue-600 to-blue-500 border-b border-blue-700 overflow-hidden">
      <!-- AI Background Pattern - Right side only -->
      <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
        <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="tools-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="1" fill="white"/>
              <path d="M5,5 L15,15 M15,5 L5,15" stroke="white" stroke-width="0.5"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#tools-pattern)"/>
        </svg>
      </div>
      
      <!-- Neural Network Background - Right side concentrated -->
      <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
        <div class="w-full h-full" style="background-image: radial-gradient(circle at 80% 30%, white 2px, transparent 2px), radial-gradient(circle at 90% 70%, white 2px, transparent 2px), radial-gradient(circle at 75% 50%, white 1px, transparent 1px); background-size: 40px 40px, 25px 25px, 60px 60px;"></div>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-blue-500 rounded-2xl flex items-center justify-center mr-6 border border-blue-700">
              <img 
                src="/external-tools-logo.png"
                alt="External Tools"
                class="w-10 h-10 object-contain"
                @error="iconError = true"
              />
              <UIcon v-if="iconError" name="i-heroicons-building-office" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Approved External Tools</h1>
              <p class="text-xl text-blue-100">Enterprise-Ready AI Services Collection</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">

      <!-- About Section -->
      <div class="mb-8">
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">About Approved METRO Tools</h2>
          
          <div class="prose prose-lg max-w-none text-gray-700 mb-8">
            <p class="text-lg leading-relaxed">
              This collection contains <strong>officially approved AI services</strong> from METRO AG that meet our enterprise security, 
              compliance, and data protection standards. These tools are <strong>safe to use for business operations</strong> and will be 
              continuously expanded with new services.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Enterprise Security -->
            <div class="space-y-3">
              <h3 class="text-xl font-bold text-gray-900">Enterprise Security & Compliance</h3>
              <p class="text-gray-700 leading-relaxed">
                All tools in this collection undergo rigorous security reviews and comply with METRO AG's data protection policies, 
                ensuring safe use for confidential business data.
              </p>
            </div>
            
            <!-- Continuous Expansion -->
            <div class="space-y-3">
              <h3 class="text-xl font-bold text-gray-900">Continuous Expansion</h3>
              <p class="text-gray-700 leading-relaxed">
                This collection will grow over time as we evaluate and approve new AI services that can enhance productivity 
                while maintaining our high security standards.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Tools Section -->
      <div class="mb-8">
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Available Tools</h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Copilot M365 Chat -->
            <div class="bg-gradient-to-br from-orange-50 to-orange-100 border border-orange-200 rounded-xl p-6">
              <div class="flex items-start space-x-4 mb-4">
                <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm">
                  <img 
                    src="/copilot_icon.png" 
                    alt="Copilot M365" 
                    class="w-8 h-8 object-contain"
                  />
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-gray-900 mb-2">Copilot M365 Chat</h3>
                  <p class="text-gray-700 text-sm mb-4">
                    Your approved AI assistant for workplace productivity. Chat, summarize documents, and get help with daily tasks 
                    through Microsoft's secure platform.
                  </p>
                </div>
              </div>
              
              <div class="space-y-3">
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-shield-check" class="w-4 h-4 text-green-600" />
                  <span>Enterprise data protection</span>
                </div>
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-chat-bubble-left-right" class="w-4 h-4 text-blue-600" />
                  <span>Conversational AI assistant</span>
                </div>
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-document-text" class="w-4 h-4 text-purple-600" />
                  <span>Document analysis & summarization</span>
                </div>
              </div>
              
              <div class="mt-6">
                <a
                  href="https://m365.cloud.microsoft/"
                  target="_blank"
                  rel="noopener noreferrer"
                  @click="trackButtonClick('Launch Copilot M365 Chat', { toolType: 'copilot', linkType: 'external', destination: 'microsoft_m365' })"
                  class="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-medium rounded-lg shadow-md hover:from-blue-700 hover:to-blue-800 hover:shadow-lg transition-all cursor-pointer"
                >
                  <UIcon name="i-heroicons-arrow-top-right-on-square" class="w-4 h-4" />
                  <span>Launch Copilot Chat</span>
                </a>
              </div>
            </div>

            <!-- LING AI Translation -->
            <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 border border-emerald-200 rounded-xl p-6">
              <div class="flex items-start space-x-4 mb-4">
                <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm">
                  <UIcon name="i-heroicons-language" class="w-8 h-8 text-emerald-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-gray-900 mb-2">LING AI Translation</h3>
                  <p class="text-gray-700 text-sm mb-4">
                    Professional document translation service for Microsoft Office files. Upload Word, Excel, or PowerPoint documents 
                    and translate them into multiple languages while preserving formatting.
                  </p>
                </div>
              </div>
              
              <div class="space-y-3">
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-document-arrow-up" class="w-4 h-4 text-blue-600" />
                  <span>Word, Excel, PowerPoint support</span>
                </div>
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-globe-europe-africa" class="w-4 h-4 text-emerald-600" />
                  <span>Multiple language support</span>
                </div>
                <div class="flex items-center space-x-2 text-sm text-gray-600">
                  <UIcon name="i-heroicons-sparkles" class="w-4 h-4 text-purple-600" />
                  <span>Preserves original formatting</span>
                </div>
              </div>
              
              <div class="mt-6">
                <a
                  href="https://your-translation-tool.example.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  @click="trackButtonClick('Launch LING AI Translation', { toolType: 'ling_ai', linkType: 'external', destination: 'ling_ai_metro' })"
                  class="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-emerald-600 to-emerald-700 text-white font-medium rounded-lg shadow-md hover:from-emerald-700 hover:to-emerald-800 hover:shadow-lg transition-all cursor-pointer"
                >
                  <UIcon name="i-heroicons-arrow-top-right-on-square" class="w-4 h-4" />
                  <span>Start Translation</span>
                </a>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Guidelines & Support Section -->
      <div class="mb-8">
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Guidelines & Support</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- AI Introduction E-Trainings -->
            <a
              href="https://your-learning-platform.example.com/ai-training"
              target="_blank"
              rel="noopener noreferrer"
              @click="trackButtonClick('AI Introduction E-Trainings', { linkType: 'external', destination: 'learning_platform' })"
              class="group p-6 bg-gray-50 border border-gray-200 rounded-xl hover:bg-gray-100 hover:border-gray-300 transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between mb-3">
                <h3 class="font-semibold text-gray-900 group-hover:text-gray-700 transition-colors">AI Introduction E-Trainings</h3>
                <UIcon name="i-heroicons-arrow-top-right-on-square" class="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" />
              </div>
              <p class="text-sm text-gray-600">Learn the fundamentals of AI in the workplace</p>
            </a>

            <!-- Team Community -->
            <a
              href="https://your-community-platform.example.com"
              target="_blank"
              rel="noopener noreferrer"
              @click="trackButtonClick('Team Community', { linkType: 'external', destination: 'community_platform' })"
              class="group p-6 bg-gray-50 border border-gray-200 rounded-xl hover:bg-gray-100 hover:border-gray-300 transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between mb-3">
                <h3 class="font-semibold text-gray-900 group-hover:text-gray-700 transition-colors">Viva Engage Community</h3>
                <UIcon name="i-heroicons-arrow-top-right-on-square" class="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" />
              </div>
              <p class="text-sm text-gray-600">Connect with colleagues and share AI experiences</p>
            </a>

            <!-- AI Guidelines -->
            <a
              href="https://your-intranet.example.com/ai-guidelines"
              target="_blank"
              rel="noopener noreferrer"
              @click="trackButtonClick('AI Guidelines', { linkType: 'external', destination: 'ai_guidelines' })"
              class="group p-6 bg-gray-50 border border-gray-200 rounded-xl hover:bg-gray-100 hover:border-gray-300 transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between mb-3">
                <h3 class="font-semibold text-gray-900 group-hover:text-gray-700 transition-colors">AI Guidelines</h3>
                <UIcon name="i-heroicons-arrow-top-right-on-square" class="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" />
              </div>
              <p class="text-sm text-gray-600">Review official AI usage guidelines and standards</p>
            </a>
          </div>
        </div>
      </div>

      <!-- Tips Section -->
      <div class="mt-8 border border-blue-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(59, 130, 246, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-blue-800" />
          <h3 class="text-xl font-bold text-blue-900">Tips for Using METRO Tools</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-blue-800">Getting Started</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Log in with your company Microsoft account</li>
              <li>• All tools are pre-approved for business use</li>
              <li>• Use these tools confidently for work tasks</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-blue-800">Best Practices</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Follow company AI usage guidelines</li>
              <li>• Check for new tools added regularly</li>
              <li>• Share feedback on tool effectiveness</li>
            </ul>
          </div>
        </div>
      </div>
    </UContainer>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// State
const iconError = ref(false)
const authStore = useAuthStore()

// Adobe Tracking
const { trackButtonClick } = useAdobeTracking()

// Client-side auth check and redirect
onMounted(async () => {
  // Wait for auth store to be initialized
  if (!authStore.isInitialized) {
    await authStore.init()
  }
  
  // Redirect to login if not authenticated
  if (!authStore.isAuthenticated) {
    await navigateTo('/login')
    return
  }
})

// Watch for auth state changes
watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
  if (!isAuthenticated) {
    navigateTo('/login')
  }
})

// SEO
useHead({
  title: 'Approved METRO Tools - DAISY',
  meta: [
    {
      name: 'description',
      content: 'Collection of approved and enterprise-ready AI services from METRO AG for secure business use. Access Copilot M365 Chat and LING AI translation services.'
    }
  ]
})
</script> 