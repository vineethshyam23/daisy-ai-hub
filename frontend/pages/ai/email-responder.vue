<template>
  <!-- Loading State while auth is being determined -->
  <div v-if="!authStore.isInitialized" class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50 flex items-center justify-center">
    <div class="text-center">
      <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl animate-pulse">
        <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
      </div>
              <h2 class="text-2xl font-bold bg-gradient-to-r from-orange-500 to-amber-500 bg-clip-text text-transparent mb-2">
          DAISY
        </h2>
      <p class="text-gray-600 font-light">Loading Email Responder...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-indigo-50 via-indigo-25 to-blue-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-indigo-800 via-indigo-600 to-indigo-500 border-b border-indigo-700 overflow-hidden">
      <!-- Email Pattern -->
      <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
        <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="email-pattern" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
              <rect x="8" y="8" width="9" height="6" fill="none" stroke="white" stroke-width="0.5"/>
              <path d="M8,8 L12.5,11 L17,8" stroke="white" stroke-width="0.5" fill="none"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#email-pattern)"/>
        </svg>
      </div>
      
      <!-- Communication Network Background -->
      <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
        <div class="w-full h-full" style="background-image: radial-gradient(circle at 80% 25%, white 2px, transparent 2px), radial-gradient(circle at 90% 75%, white 1.5px, transparent 1.5px), radial-gradient(circle at 75% 50%, white 1px, transparent 1px); background-size: 45px 45px, 30px 30px, 60px 60px;"></div>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-indigo-500 rounded-2xl flex items-center justify-center mr-6 border border-indigo-700">
              <UIcon name="i-heroicons-envelope" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Email Responder</h1>
              <p class="text-xl text-indigo-100">Generate professional email responses with AI assistance</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">
      
      <!-- Email Input Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Original Email -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <div class="flex items-center space-x-2 mb-6">
            <UIcon name="i-heroicons-inbox" class="text-2xl text-indigo-600" />
            <h2 class="text-2xl font-bold text-gray-900">Original Email</h2>
          </div>
          
          <div class="space-y-4">
            <!-- Email Subject -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
              <input
                v-model="originalEmail.subject"
                type="text"
                placeholder="Enter the email subject..."
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg"
              />
            </div>
            
            <!-- Email Sender -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">From</label>
              <input
                v-model="originalEmail.sender"
                type="email"
                placeholder="sender@example.com"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg"
              />
            </div>
            
            <!-- Email Content -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email Content</label>
              <textarea
                v-model="originalEmail.content"
                placeholder="Paste the original email content here..."
                rows="8"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg font-mono resize-y min-h-[200px]"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Reply Configuration -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <div class="flex items-center space-x-2 mb-6">
            <UIcon name="i-heroicons-cog-6-tooth" class="text-2xl text-indigo-600" />
            <h2 class="text-2xl font-bold text-gray-900">Reply Settings</h2>
          </div>
          
          <div class="space-y-4">
            <!-- Tone Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tone</label>
              <select
                v-model="replySettings.tone"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="Professional">Professional - Business standard tone</option>
                <option value="Friendly">Friendly - Warm and approachable</option>
                <option value="Formal">Formal - Official and structured</option>
                <option value="Casual">Casual - Relaxed and informal</option>
                <option value="Apologetic">Apologetic - Sorry and understanding</option>
                <option value="Confident">Confident - Assertive and sure</option>
                <option value="Collaborative">Collaborative - Team-oriented</option>
                <option value="Urgent">Urgent - Time-sensitive</option>
                <option value="Enthusiastic">Enthusiastic - Excited and positive</option>
              </select>
            </div>
            
            <!-- Reply Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Reply Type</label>
              <select
                v-model="replySettings.type"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="Response">Response - Direct answer to inquiry</option>
                <option value="Acknowledgment">Acknowledgment - Confirm receipt</option>
                <option value="Follow-up">Follow-up - Continue conversation</option>
                <option value="Decline">Decline - Politely refuse request</option>
                <option value="Request Information">Request Information - Ask for details</option>
                <option value="Schedule Meeting">Schedule Meeting - Propose meeting</option>
                <option value="Provide Update">Provide Update - Share status</option>
                <option value="Redirect">Redirect - Forward to colleague</option>
                <option value="Set Expectations">Set Expectations - Timeline clarification</option>
                <option value="Proposal">Proposal - Suggest solution</option>
              </select>
            </div>
            
            <!-- Length -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Length</label>
              <select
                v-model="replySettings.length"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="Brief">Brief - Quick and concise (1-2 sentences)</option>
                <option value="Medium">Medium - Standard response (1-2 paragraphs)</option>
                <option value="Detailed">Detailed - Comprehensive (3+ paragraphs)</option>
                <option value="Bullet Points">Bullet Points - Structured list format</option>
              </select>
            </div>
            
            <!-- Priority -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                v-model="replySettings.priority"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="High">High - Urgent response needed</option>
                <option value="Normal">Normal - Standard priority</option>
                <option value="Low">Low - No rush, when convenient</option>
                <option value="Auto">Auto - Let AI determine priority</option>
              </select>
            </div>
            
            <!-- Additional Instructions -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Additional Instructions</label>
              <textarea
                v-model="replySettings.instructions"
                placeholder="Any specific points to address or tone adjustments..."
                rows="4"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none transition-colors text-lg resize-y min-h-[100px]"
              ></textarea>
            </div>
            
            <!-- Generate Button -->
            <div class="pt-4">
              <UButton 
                @click="generateReply"
                :loading="isGenerating"
                :disabled="tokenStore.isTokenDataReady && !tokenStore.hasTokensForAssistant('email-reply')"
                color="primary"
                size="xl"
                :class="[
                  'w-full font-semibold transition-all duration-300',
                  (!tokenStore.isTokenDataReady || tokenStore.hasTokensForAssistant('email-reply'))
                    ? 'bg-indigo-600 hover:bg-indigo-700 text-white cursor-pointer' 
                    : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                ]"
                icon="i-heroicons-sparkles"
              >
                <span v-if="isGenerating">Generating Reply...</span>
                <span v-else-if="!tokenStore.isTokenDataReady">Loading tokens...</span>
                <span v-else-if="!tokenStore.hasTokensForAssistant('email-reply')">
                  Insufficient Tokens ({{ tokenStore.getTokenCost('email-reply') }} required)
                </span>
                <span v-else>
                  Generate Reply ({{ tokenStore.getTokenCost('email-reply') }} token)
                </span>
              </UButton>
              
              <!-- Token Warning -->
              <div v-if="tokenStore.isTokenDataReady && !tokenStore.canUseTokens" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-exclamation-triangle" class="w-4 h-4 text-red-500" />
                  <span class="text-red-700 text-sm font-medium">No tokens remaining</span>
                </div>
                <p class="text-red-600 text-xs mt-1">
                  Your daily tokens will reset in {{ tokenStore.getHoursUntilReset() }} hours
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <DisclaimerBox 
        disclaimer-text="This email is drafted by AI and may need a quick review to make sure it fits your tone and intent. Please review before sending."
        class="mb-6"
      />

      <!-- Modern Loading State -->
      <div v-if="isGenerating" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-indigo-200 border-t-indigo-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-envelope" class="text-2xl text-indigo-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-indigo-600" />
            <h3 class="text-2xl font-bold text-gray-900">Crafting Your Reply</h3>
          </div>
          <p class="text-gray-600 mb-8">This may take a few seconds...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-indigo-100 rounded-full h-3">
              <div 
                class="bg-indigo-600 h-3 rounded-full transition-all duration-500" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-indigo-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Generated Reply Section -->
      <div v-if="generatedReply" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-2">
            <UIcon name="i-heroicons-paper-airplane" class="text-2xl text-indigo-600" />
            <h2 class="text-2xl font-bold text-gray-900">Generated Reply</h2>
          </div>
          <div class="flex space-x-3">
            <div class="relative">
              <UButton
                @click="copyReply"
                variant="outline"
                class="cursor-pointer px-4 py-2 border border-gray-300 hover:border-indigo-500 hover:bg-indigo-50 transition-all duration-200 group"
              >
                <UIcon name="i-heroicons-document-duplicate" class="w-5 h-5 text-gray-600 group-hover:text-indigo-600 mr-2" />
                <span class="text-gray-700 group-hover:text-indigo-700 font-medium">Copy Reply</span>
              </UButton>
              <!-- Copy Confirmation Text -->
              <div v-if="copyConfirmation" class="absolute top-full mt-2 left-0 z-50 text-sm text-indigo-600 font-medium flex items-center space-x-1 whitespace-nowrap bg-white px-3 py-2 rounded-lg shadow-lg border border-indigo-200">
                <UIcon name="i-heroicons-check-circle" class="w-4 h-4" />
                <span>Reply copied to clipboard!</span>
              </div>
            </div>
            <UButton
              @click="regenerateReply"
              variant="outline"
              :disabled="isRegenerating"
              :class="[
                'px-4 py-2 border transition-all duration-200 group',
                isRegenerating 
                  ? 'border-gray-300 bg-gray-100 text-gray-500 cursor-not-allowed'
                  : 'border-gray-300 hover:border-indigo-500 hover:bg-indigo-50 cursor-pointer'
              ]"
            >
              <UIcon 
                :name="isRegenerating ? 'i-heroicons-arrow-path' : 'i-heroicons-arrow-path'" 
                class="w-5 h-5 mr-2"
                :class="[
                  isRegenerating ? 'text-gray-500 animate-spin' : 'text-gray-600 group-hover:text-indigo-600'
                ]"
              />
              <span 
                :class="[
                  isRegenerating ? 'text-gray-500' : 'text-gray-700 group-hover:text-indigo-700 font-medium'
                ]"
              >
                {{ isRegenerating ? 'Regenerating...' : 'Regenerate' }}
              </span>
            </UButton>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 border border-gray-200">
          <div class="space-y-4">
            <!-- Email Headers -->
            <div class="border-b border-gray-200 pb-3">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-envelope" class="text-gray-400" />
                  <span class="text-gray-600">Subject:</span>
                  <span class="font-medium text-gray-800">Re: {{ originalEmail.subject }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <UIcon name="i-heroicons-user" class="text-gray-400" />
                  <span class="text-gray-600">To:</span>
                  <span class="font-medium text-gray-800">{{ originalEmail.sender || 'recipient@example.com' }}</span>
                </div>
              </div>
            </div>
            
            <!-- Email Body -->
            <div class="min-h-[200px]">
              <div class="prose prose-lg max-w-none">
                <div class="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed text-base">{{ generatedReply }}</div>
              </div>
            </div>
            
            <!-- Email Footer -->
            <div class="border-t border-gray-200 pt-3">
              <div class="flex items-center justify-between text-sm text-gray-500">
                <div class="flex items-center space-x-4">
                  <span class="flex items-center space-x-1">
                    <UIcon name="i-heroicons-cog-6-tooth" class="w-4 h-4" />
                    <span>{{ replySettings.tone }} tone</span>
                  </span>
                  <span class="flex items-center space-x-1">
                    <UIcon name="i-heroicons-document-text" class="w-4 h-4" />
                    <span>{{ replySettings.length }} length</span>
                  </span>
                  <span class="flex items-center space-x-1">
                    <UIcon name="i-heroicons-flag" class="w-4 h-4" />
                    <span>{{ replySettings.priority }} priority</span>
                  </span>
                </div>
                <span class="text-xs text-gray-400">Generated by AI</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tips Section -->
      <div class="mt-8 border border-indigo-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(99, 102, 241, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-indigo-800" />
          <h3 class="text-xl font-bold text-indigo-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-indigo-800">Email Content</h4>
            <ul class="text-sm text-indigo-700 space-y-1">
              <li>• Include the complete original email</li>
              <li>• Provide context about your relationship</li>
              <li>• Mention any urgency or deadlines</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-indigo-800">Settings</h4>
            <ul class="text-sm text-indigo-700 space-y-1">
              <li>• Choose appropriate tone for relationship</li>
              <li>• Specify key points to address</li>
              <li>• Adjust length based on context</li>
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
import { useTokenStore } from '~/stores/tokens'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Stores
const authStore = useAuthStore()
const tokenStore = useTokenStore()

// Adobe Tracking
const { trackButtonClick } = useAdobeTracking()

// Initialize stores after navigation (auth is handled by middleware)
onMounted(async () => {
  // Initialize token store after successful authentication
  if (!tokenStore.isInitialized) {
    await tokenStore.init()
  }
})

// State
const originalEmail = ref({
  subject: '',
  sender: '',
  content: ''
})

const replySettings = ref({
  tone: 'Professional',
  type: 'Response',
  length: 'Medium',
  priority: 'Normal',
  instructions: ''
})

const generatedReply = ref('')
const isGenerating = ref(false)
const copyConfirmation = ref(false)
const isRegenerating = ref(false) // Track loading state for regenerate button
const progress = ref(0)
const progressText = ref('')

// Native select elements are now used instead of USelect for better compatibility

// Methods
const updateProgressText = () => {
  const texts = [
    'Analyzing email content...',
    'Understanding context...',
    'Crafting response...',
    'Polishing tone and style...',
    'Finalizing reply...',
    'Almost ready...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

const generateReply = async () => {
  if (!originalEmail.value.content.trim()) {
    const toast = useToast()
    toast.add({
      title: 'Missing Content',
      description: 'Please enter the original email content before generating a reply.',
      color: 'red'
    })
    return
  }

  if (!originalEmail.value.subject.trim()) {
    const toast = useToast()
    toast.add({
      title: 'Missing Subject',
      description: 'Please enter the email subject before generating a reply.',
      color: 'red'
    })
    return
  }

  // Check if user has sufficient tokens
  if (!tokenStore.hasTokensForAssistant('email-reply')) {
    const toast = useToast()
    toast.add({
      title: 'Insufficient Tokens',
      description: `You need ${tokenStore.getTokenCost('email-reply')} token(s) to use this assistant. Your tokens will reset in ${tokenStore.getHoursUntilReset()} hours.`,
      color: 'red',
      timeout: 8000
    })
    return
  }

  // Track button click with structured data
  trackButtonClick('Generate Email Reply', {
    tone: replySettings.value.tone,
    replyType: replySettings.value.type,
    length: replySettings.value.length,
    priority: replySettings.value.priority,
    hasInstructions: !!replySettings.value.instructions.trim(),
    hasSender: !!originalEmail.value.sender.trim(),
    subjectLength: originalEmail.value.subject.length,
    contentLength: originalEmail.value.content.length,
    tokenCost: tokenStore.getTokenCost('email-reply')
  })

  isGenerating.value = true
  progress.value = 0
  
  try {
    // Simulate progress
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 10
        updateProgressText()
      }
    }, 1000)

    // Prepare API request
    const requestBody = {
      subject: originalEmail.value.subject,
      from_sender: originalEmail.value.sender || 'sender@example.com',
      email_content: originalEmail.value.content,
      tone: replySettings.value.tone,
      reply_type: replySettings.value.type,
      length: replySettings.value.length,
      priority: replySettings.value.priority,
      additional_instructions: replySettings.value.instructions || ''
    }

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    const response = await authenticatedEndpointRequest(apiEndpoints.emailReply, {
      method: 'POST',
      body: requestBody
    })

    clearInterval(progressInterval)
    progress.value = 100
    progressText.value = 'Complete!'

    // Set the generated reply
    generatedReply.value = response.content
    
    // Consume token after successful response
    const tokenCost = tokenStore.getTokenCost('email-reply')
    const tokenConsumed = await tokenStore.useTokens(tokenCost)
    
    if (tokenConsumed) {
      // Track token usage
      const { trackTokenUsage } = useAdobeTracking()
      trackTokenUsage(tokenCost, 'email_responder', {
        replyType: replySettings.value.type,
        tone: replySettings.value.tone,
        length: replySettings.value.length,
        hasInstructions: !!replySettings.value.instructions
      })
    } else {
      console.warn('Failed to consume tokens, but response was successful')
    }
    
    // Show success notification with token info
    const toast = useToast()
    toast.add({
      title: 'Reply Generated',
      description: `Your email reply has been generated successfully. ${tokenStore.tokens} tokens remaining today.`,
      color: 'green'
    })
    
  } catch (error) {
    console.error('Error generating reply:', error)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_email_responder_failed', 'Email Responder API request failed', {
      errorMessage: error.message || error.toString(),
      errorCode: error.status || error.statusCode || 'unknown',
      errorType: error.name || 'APIError',
      endpoint: 'emailReply',
      requestData: {
        tone: replySettings.value.tone,
        replyType: replySettings.value.type,
        length: replySettings.value.length,
        priority: replySettings.value.priority,
        hasInstructions: !!replySettings.value.instructions,
        subjectLength: originalEmail.value.subject?.length || 0,
        emailContentLength: originalEmail.value.content?.length || 0
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    // Show error notification
    const toast = useToast()
    toast.add({
      title: 'Generation Failed',
      description: error.data?.message || 'Failed to generate reply. Please try again.',
      color: 'red'
    })
  } finally {
    isGenerating.value = false
    setTimeout(() => {
      progress.value = 0
      progressText.value = ''
    }, 2000)
  }
}

const copyReply = async () => {
  try {
    // Track copy action
    trackButtonClick('Copy Email Reply', {
      tone: replySettings.value.tone,
      replyType: replySettings.value.type,
      length: replySettings.value.length,
      replyLength: generatedReply.value.length,
      hasReply: !!generatedReply.value.trim()
    })

    await navigator.clipboard.writeText(generatedReply.value)
    copyConfirmation.value = true
    // Hide the confirmation after 3 seconds
    setTimeout(() => {
      copyConfirmation.value = false
    }, 3000)
  } catch (error) {
    console.error('Failed to copy:', error)
    const toast = useToast()
    toast.add({
      title: 'Copy Failed',
      description: 'Failed to copy reply to clipboard.',
      color: 'red'
    })
  }
}

const regenerateReply = async () => {
  if (!originalEmail.value.content.trim() || !originalEmail.value.subject.trim()) {
    const toast = useToast()
    toast.add({
      title: 'Missing Information',
      description: 'Please ensure original email content and subject are filled.',
      color: 'red'
    })
    return
  }

  // Check if user has sufficient tokens
  if (!tokenStore.hasTokensForAssistant('email-reply')) {
    const toast = useToast()
    toast.add({
      title: 'Insufficient Tokens',
      description: `You need ${tokenStore.getTokenCost('email-reply')} token(s) to regenerate. Your tokens will reset in ${tokenStore.getHoursUntilReset()} hours.`,
      color: 'red',
      timeout: 8000
    })
    return
  }

  // Track regenerate action
  trackButtonClick('Regenerate Email Reply', {
    tone: replySettings.value.tone,
    replyType: replySettings.value.type,
    length: replySettings.value.length,
    priority: replySettings.value.priority,
    hasInstructions: !!replySettings.value.instructions.trim(),
    previousReplyLength: generatedReply.value.length,
    tokenCost: tokenStore.getTokenCost('email-reply')
  })

  isRegenerating.value = true
  
  try {
    // Prepare API request
    const requestBody = {
      subject: originalEmail.value.subject,
      from_sender: originalEmail.value.sender || 'sender@example.com',
      email_content: originalEmail.value.content,
      tone: replySettings.value.tone,
      reply_type: replySettings.value.type,
      length: replySettings.value.length,
      priority: replySettings.value.priority,
      additional_instructions: replySettings.value.instructions || ''
    }

    // Make authenticated API call
    const { authenticatedEndpointRequest, apiEndpoints } = await import('~/config/api.config')
    const response = await authenticatedEndpointRequest(apiEndpoints.emailReply, {
      method: 'POST',
      body: requestBody
    })

    // Set the new generated reply
    generatedReply.value = response.content
    
    // Consume token after successful response
    const tokenCost = tokenStore.getTokenCost('email-reply')
    const tokenConsumed = await tokenStore.useTokens(tokenCost)
    
    if (tokenConsumed) {
      // Track token usage
      const { trackTokenUsage } = useAdobeTracking()
      trackTokenUsage(tokenCost, 'email_responder', {
        replyType: replySettings.value.type,
        tone: replySettings.value.tone,
        length: replySettings.value.length,
        hasInstructions: !!replySettings.value.instructions,
        isRegeneration: true
      })
    } else {
      console.warn('Failed to consume tokens, but response was successful')
    }
    
    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'Reply Regenerated',
      description: `Your email reply has been regenerated successfully. ${tokenStore.tokens} tokens remaining today.`,
      color: 'green'
    })
    
  } catch (error) {
    console.error('Error regenerating reply:', error)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_email_responder_regenerate_failed', 'Email Responder regenerate API request failed', {
      errorMessage: error.message || error.toString(),
      errorCode: error.status || error.statusCode || 'unknown',
      errorType: error.name || 'APIError',
      endpoint: 'emailReply',
      action: 'regenerate',
      requestData: {
        tone: replySettings.value.tone,
        replyType: replySettings.value.type,
        length: replySettings.value.length,
        priority: replySettings.value.priority,
        hasInstructions: !!replySettings.value.instructions,
        subjectLength: originalEmail.value.subject?.length || 0,
        emailContentLength: originalEmail.value.content?.length || 0,
        previousReplyLength: generatedReply.value?.length || 0
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    // Show error notification
    const toast = useToast()
    toast.add({
      title: 'Regeneration Failed',
      description: error.data?.message || 'Failed to regenerate reply. Please try again.',
      color: 'red'
    })
  } finally {
    isRegenerating.value = false
  }
}

// SEO
useHead({
  title: 'Email Responder - DAISY',
  meta: [
    { name: 'description', content: 'Generate professional email responses with AI assistance. Save time and improve your communication.' }
  ]
})
</script> 