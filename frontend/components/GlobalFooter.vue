<template>
  <div class="bg-white/90 backdrop-blur-sm border-t border-orange-200 mt-20">
    <UContainer class="py-12">
      <div class="flex flex-col items-center justify-center space-y-6">
        <!-- Logo und Copyright -->
        <div class="flex items-center space-x-4">
          <img 
            src="/logo.png" 
            alt="AI Hub Logo"
            class="h-8 w-auto"
            @error="footerLogoError = true"
          />
          <div v-if="footerLogoError" class="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center">
            <UIcon name="i-heroicons-cpu-chip" class="w-5 h-5 text-white" />
          </div>
          <span class="text-gray-600 font-light">© 2025 AI Hub</span>
        </div>
        
        <!-- Links -->
        <div class="flex items-center justify-center space-x-4">
          <a 
            href="https://forms.office.com/Pages/ResponsePage.aspx?id=CCMyZKkJo0eMHLgocdYFaOQEH56T8uxKi30gB-Um1R5UMURZTTNFUEZPNTE3SENWSllTWVI5V0lTTi4u"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center space-x-2 text-gray-600 hover:text-orange-500 transition-colors duration-200 font-medium"
            @click="trackFooterClick('feedback')"
          >
            <UIcon name="i-heroicons-chat-bubble-left-right" class="w-4 h-4" />
            <span>Feedback</span>
          </a>
          
          <span class="text-gray-400 font-light">|</span>
          
          <a 
            href="https://forms.office.com/Pages/ResponsePage.aspx?id=CCMyZKkJo0eMHLgocdYFaOQEH56T8uxKi30gB-Um1R5UQ1VRSFk3OUtWQ09QNFA0R0hDRVZKTk80OS4u"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center space-x-2 text-gray-600 hover:text-orange-500 transition-colors duration-200 font-medium"
            @click="trackFooterClick('get_assistant')"
          >
            <UIcon name="i-heroicons-sparkles-20-solid" class="w-4 h-4" />
            <span>Get your own assistant!</span>
          </a>
        </div>
        
        <!-- Acceptable Use Policy -->
        <div class="flex items-center justify-center">
          <a 
            href="/Acceptable_Use_Policy.pdf"
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-600 hover:text-orange-500 transition-colors duration-200 font-medium"
            @click="trackFooterClick('aup')"
          >
            Acceptable Use Policy (AUP)
          </a>
        </div>
      </div>
    </UContainer>
  </div>
</template>

<script setup>
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Footer state
const footerLogoError = ref(false)

// Adobe Tracking
const { trackButtonClick } = useAdobeTracking()

// Footer tracking
const trackFooterClick = (linkType) => {
  try {
    const destination = linkType === 'aup' ? 'pdf_document' : 'microsoft_forms'
    trackButtonClick(`Footer ${linkType} Link`, {
      linkType: linkType,
      destination: destination,
      currentPage: useRoute().path
    })
  } catch (error) {
    console.error('Tracking error:', error)
  }
}
</script> 