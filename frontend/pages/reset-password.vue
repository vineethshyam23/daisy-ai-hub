<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-red-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-lock-closed" class="w-8 h-8 text-orange-600" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Reset Password</h1>
          <p class="text-gray-600">Create a new password for your account</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Verifying reset link...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-8">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-exclamation-triangle" class="w-8 h-8 text-red-600" />
          </div>
          <h2 class="text-xl font-semibold text-gray-900 mb-2">Invalid Reset Link</h2>
          <p class="text-gray-600 mb-6">{{ error }}</p>
          <button
            @click="() => window.location.href = '/login'"
            class="px-6 py-3 bg-orange-600 text-white font-medium rounded-lg hover:bg-orange-700 transition-colors"
          >
            Back to Login
          </button>
        </div>

        <!-- Success State -->
        <div v-else-if="resetSuccessful" class="text-center py-8">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-check-circle" class="w-8 h-8 text-green-600" />
          </div>
          <h2 class="text-xl font-semibold text-gray-900 mb-2">Password Reset Successful!</h2>
          <p class="text-gray-600 mb-6">Your password has been updated successfully.</p>
          <button
            @click="() => window.location.href = '/login'"
            class="px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
          >
            Go to Login
          </button>
        </div>

        <!-- Reset Form -->
        <div v-else>
          <div class="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-center">
              <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-blue-600 mr-2" />
              <div>
                <p class="text-blue-800 font-medium text-sm">Reset for: {{ verifiedEmail }}</p>
                <p class="text-blue-600 text-sm">Enter your new password below</p>
              </div>
            </div>
          </div>

          <form @submit.prevent="handlePasswordReset" class="space-y-6">
            <div>
              <label for="new-password" class="block text-sm font-medium text-gray-700 mb-2">
                New Password
              </label>
              <div class="relative">
                <input
                  id="new-password"
                  v-model="newPassword"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  :disabled="authStore.loading"
                  placeholder="Enter your new password"
                  class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <UIcon
                    :name="showPassword ? 'i-heroicons-eye-slash' : 'i-heroicons-eye'"
                    class="w-5 h-5 text-gray-400 hover:text-gray-600"
                  />
                </button>
              </div>
              <p class="text-sm text-gray-500 mt-1">Password must be at least 6 characters long</p>
            </div>

            <div>
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                Confirm New Password
              </label>
              <input
                id="confirm-password"
                v-model="confirmPassword"
                type="password"
                required
                :disabled="authStore.loading"
                placeholder="Confirm your new password"
                class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>

            <!-- Password Match Validation -->
            <div v-if="confirmPassword && newPassword !== confirmPassword" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <div class="flex items-center">
                <UIcon name="i-heroicons-exclamation-triangle" class="w-4 h-4 text-red-500 mr-2" />
                <p class="text-red-700 text-sm">Passwords do not match</p>
              </div>
            </div>

            <button
              type="submit"
              :disabled="!isFormValid || authStore.loading"
              class="w-full px-4 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-red-600 focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <UIcon v-if="authStore.loading" name="i-heroicons-arrow-path" class="w-4 h-4 mr-2 animate-spin" />
              <span>{{ authStore.loading ? 'Updating Password...' : 'Update Password' }}</span>
            </button>
          </form>

          <!-- Error Display -->
          <div v-if="authStore.error" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex justify-between items-start">
              <div class="flex">
                <UIcon name="i-heroicons-exclamation-triangle" class="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 class="text-red-800 font-medium text-sm">Error</h4>
                  <p class="text-red-600 text-sm mt-1">{{ authStore.error }}</p>
                </div>
              </div>
              <button @click="authStore.error = null" class="text-red-400 hover:text-red-600">
                <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Back to Login -->
        <div class="text-center mt-8">
          <button
            @click="() => window.location.href = '/login'"
            class="text-orange-600 hover:text-orange-500 font-medium text-sm"
          >
            ← Back to Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

const authStore = useAuthStore()
const { trackPasswordRecovery, trackError } = useAdobeTracking()

// State
const loading = ref(true)
const error = ref('')
const resetSuccessful = ref(false)
const verifiedEmail = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const resetCode = ref('')

// Computed
const isFormValid = computed(() => {
  return newPassword.value.length >= 6 && 
         newPassword.value === confirmPassword.value &&
         resetCode.value
})

// Methods
const handlePasswordReset = async () => {
  try {
    trackPasswordRecovery(verifiedEmail.value, 'reset_attempt', {
      emailDomain: verifiedEmail.value.split('@')[1] || 'unknown',
      passwordLength: newPassword.value.length
    })

    await authStore.confirmPasswordReset(resetCode.value, newPassword.value)
    resetSuccessful.value = true
    
    trackPasswordRecovery(verifiedEmail.value, 'reset_success', {
      emailDomain: verifiedEmail.value.split('@')[1] || 'unknown',
      passwordLength: newPassword.value.length
    })
  } catch (error) {
    console.error('Password reset failed:', error)
    
    trackError('auth_password_reset_failed', error.message || error.toString(), {
      emailDomain: verifiedEmail.value.split('@')[1] || 'unknown',
      resetCode: !!resetCode.value,
      passwordLength: newPassword.value.length,
      errorCode: error.code || 'unknown'
    })
  }
}

// Initialize
onMounted(async () => {
  const route = useRoute()
  
  // Get the reset code from URL parameters
  const oobCode = route.query.oobCode
  const mode = route.query.mode
  
  if (!oobCode || mode !== 'resetPassword') {
    error.value = 'Invalid or missing reset code. Please request a new password reset.'
    loading.value = false
    return
  }
  
  resetCode.value = oobCode
  
  try {
    // Verify the reset code and get the email
    const email = await authStore.verifyResetCode(oobCode)
    verifiedEmail.value = email
    loading.value = false
    
    trackPasswordRecovery(email, 'reset_page_accessed', {
      emailDomain: email.split('@')[1] || 'unknown',
      hasValidCode: true
    })
  } catch (error) {
    console.error('Reset code verification failed:', error)
    
    trackError('auth_password_reset_code_invalid', error.message || error.toString(), {
      hasCode: !!oobCode,
      mode: mode || 'unknown',
      errorCode: error.code || 'unknown'
    })
    
    if (error.code === 'auth/expired-action-code') {
      error.value = 'This password reset link has expired. Please request a new one.'
    } else if (error.code === 'auth/invalid-action-code') {
      error.value = 'This password reset link is invalid. Please request a new one.'
    } else {
      error.value = 'Unable to verify reset link. Please try again or request a new reset email.'
    }
    
    loading.value = false
  }
})

// SEO
useHead({
  title: 'Reset Password - DAISY',
  meta: [
    { name: 'description', content: 'Reset your password for DAISY account access.' }
  ]
})
</script> 