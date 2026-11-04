<template>
    <div class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <!-- Header -->
        <div class="text-center">
          <div class="flex justify-center mb-6">
            <img 
              src="/logo.png" 
              alt="AI Hub Logo"
              class="h-12 w-auto"
              @error="logoError = true"
            />
            <div v-if="logoError" class="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center shadow-lg">
              <span class="text-white text-xl font-bold">D</span>
            </div>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Welcome back</h2>
          <p class="text-gray-600">Sign in to your DAISY account</p>
        </div>
  
        <!-- Login Form -->
        <div class="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-8 border border-orange-100">
          <!-- Tab Navigation -->
          <div class="flex mb-6">
            <button
              @click="() => { 
                trackButtonClick('Switch Authentication Tab', { 
                  newTab: 'login',
                  previousTab: activeTab
                }); 
                activeTab = 'login'; 
              }"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-lg mr-2 transition-all cursor-pointer',
                activeTab === 'login' 
                  ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              Sign In
            </button>
            <button
              @click="() => { 
                trackButtonClick('Switch Authentication Tab', { 
                  newTab: 'register',
                  previousTab: activeTab
                }); 
                activeTab = 'register'; 
              }"
              :class="[
                'flex-1 py-2 px-4 text-sm font-medium rounded-lg ml-2 transition-all cursor-pointer',
                activeTab === 'register' 
                  ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              Sign Up
            </button>
          </div>
  
          <!-- Login Tab -->
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Email address
              </label>
              <input
                id="email"
                v-model="loginForm.email"
                type="email"
                required
                :disabled="authStore.loading"
                placeholder="Enter your email"
                class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
  
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="loginForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  :disabled="authStore.loading"
                  placeholder="Enter your password"
                  class="w-full px-4 py-3 pr-12 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 cursor-pointer"
                >
                  <UIcon :name="showPassword ? 'i-heroicons-eye-slash' : 'i-heroicons-eye'" class="w-5 h-5" />
                </button>
              </div>
            </div>
  
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember"
                  v-model="rememberMe"
                  type="checkbox"
                  class="h-4 w-4 text-orange-500 focus:ring-orange-400 border-orange-300 rounded"
                />
                <label for="remember" class="ml-2 block text-sm text-gray-700">
                  Remember me
                </label>
              </div>
              <div class="text-sm">
                <button
                  type="button"
                  @click="() => { 
                    trackButtonClick('Open Forgot Password Modal', { 
                      currentTab: activeTab 
                    }); 
                    showForgotPasswordModal = true; 
                  }"
                  class="text-orange-600 hover:text-orange-500 font-medium cursor-pointer"
                >
                  Forgot password?
                </button>
              </div>
            </div>
  
            <button
              type="submit"
              :disabled="!isLoginFormValid || authStore.loading"
              class="w-full flex justify-center items-center px-4 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
            >
              <UIcon v-if="authStore.loading" name="i-heroicons-arrow-path" class="w-5 h-5 mr-2 animate-spin" />
              <span>{{ authStore.loading ? 'Signing in...' : 'Sign in' }}</span>
            </button>
          </form>
  
          <!-- Register Tab -->
          <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="space-y-6">
            <!-- Company Email Notice -->
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
              <div class="flex items-center">
                <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-orange-500 mr-2 flex-shrink-0" />
                <div>
                  <h3 class="text-orange-800 font-medium text-sm">Company Registration</h3>
                  <p class="text-orange-700 text-sm mt-1">Registration may be restricted to authorized email domains. Please use your company email address.</p>
                </div>
              </div>
            </div>
  
            <div>
              <label for="reg-email" class="block text-sm font-medium text-gray-700 mb-2">
                Email address
              </label>
              <input
                id="reg-email"
                v-model="registerForm.email"
                type="email"
                required
                :disabled="authStore.loading"
                placeholder="yourname@yourcompany.com"
                class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                :class="{ 'border-red-300 focus:ring-red-400 focus:border-red-400': registerForm.email && !isValidEmail }"
              />
              <p v-if="registerForm.email && !isValidEmail" class="mt-1 text-sm text-red-600">
                Please use an authorized email address
              </p>
            </div>
  
            <div>
              <label for="reg-password" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="reg-password"
                v-model="registerForm.password"
                type="password"
                required
                :disabled="authStore.loading"
                placeholder="Create a password (min. 6 characters)"
                class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
              />
              <p class="mt-1 text-xs text-gray-500">Password must be at least 6 characters long</p>
            </div>
  
            <div>
              <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                id="confirm-password"
                v-model="registerForm.confirmPassword"
                type="password"
                required
                :disabled="authStore.loading"
                placeholder="Confirm your password"
                class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                :class="{ 'border-red-300 focus:ring-red-400 focus:border-red-400': registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword }"
              />
              <p v-if="registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword" class="mt-1 text-sm text-red-600">
                Passwords do not match
              </p>
            </div>
  
  
            <button
              type="submit"
              :disabled="!isRegisterFormValid || authStore.loading"
              class="w-full flex justify-center items-center px-4 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
            >
              <UIcon v-if="authStore.loading" name="i-heroicons-arrow-path" class="w-5 h-5 mr-2 animate-spin" />
              <span>{{ authStore.loading ? 'Creating account...' : 'Create account' }}</span>
            </button>
          </form>
  
          <!-- Error Display -->
          <div v-if="authStore.error" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex justify-between items-start">
              <div class="flex">
                <UIcon name="i-heroicons-exclamation-triangle" class="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 class="text-red-800 font-medium text-sm">Authentication Error</h3>
                  <p class="text-red-600 text-sm mt-1">{{ getErrorMessage(authStore.error) }}</p>
                </div>
              </div>
              <button @click="authStore.error = null" class="text-red-400 hover:text-red-600 cursor-pointer">
                <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
              </button>
            </div>
          </div>
  
          <!-- Success Message -->
          <div v-if="showSuccess && activeTab === 'login'" class="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex">
              <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-400 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <h3 class="text-green-800 font-medium text-sm">
                  {{ successMessage.includes('Registration') ? 'Registration Successful!' : 'Welcome!' }}
                </h3>
                <p class="text-green-600 text-sm mt-1">
                  {{ successMessage || 'You have been successfully signed in.' }}
                </p>
                <div v-if="successMessage.includes('verify')" class="mt-2 text-green-700 text-sm">
                  <p>Didn't receive the email? Check your spam folder or 
                    <button 
                      @click="showResendModal = true" 
                      class="text-green-800 underline hover:text-green-900 font-medium cursor-pointer"
                    >
                      resend verification email
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Registration Success Message -->
          <div v-if="showSuccess && activeTab === 'register'" class="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex">
              <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-400 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <h3 class="text-green-800 font-medium text-sm">Registration Successful!</h3>
                <p class="text-green-600 text-sm mt-1">
                  {{ successMessage }}
                </p>
                <div v-if="successMessage.includes('verify')" class="mt-2 text-green-700 text-sm">
                  <p>Didn't receive the email? Check your spam folder or 
                    <button 
                      @click="showResendModal = true" 
                      class="text-green-800 underline hover:text-green-900 font-medium cursor-pointer"
                    >
                      resend verification email
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </div>
          

        </div>

        <!-- Forgot Password Modal -->
        <div v-if="showForgotPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full">
            <div class="text-center mb-6">
              <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <UIcon name="i-heroicons-lock-closed" class="w-6 h-6 text-orange-600" />
              </div>
              <h3 class="text-2xl font-bold text-gray-900 mb-2">Reset Password</h3>
              <p class="text-gray-600">Enter your email address and we'll send you a link to reset your password.</p>
            </div>

            <form @submit.prevent="handleForgotPassword" class="space-y-4">
              <div>
                <label for="reset-email" class="block text-sm font-medium text-gray-700 mb-2">
                  Email address
                </label>
                <input
                  id="reset-email"
                  v-model="forgotPasswordEmail"
                  type="email"
                  required
                  :disabled="authStore.loading"
                  placeholder="Enter your email address"
                  class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>

              <div class="flex space-x-3 pt-4">
                <button
                  type="button"
                  @click="() => { 
                    trackButtonClick('Cancel Password Reset', { 
                      modalState: passwordResetSent.value ? 'success' : 'input' 
                    }); 
                    closeForgotPasswordModal(); 
                  }"
                  :disabled="authStore.loading"
                  class="flex-1 px-4 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="!forgotPasswordEmail || authStore.loading"
                  class="flex-1 px-4 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                >
                  <UIcon v-if="authStore.loading" name="i-heroicons-arrow-path" class="w-4 h-4 mr-2 animate-spin" />
                  <span>{{ authStore.loading ? 'Sending...' : 'Send Reset Link' }}</span>
                </button>
              </div>
            </form>

            <!-- Success State in Modal -->
            <div v-if="passwordResetSent" class="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
              <div class="flex">
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-400 mr-2 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 class="text-green-800 font-medium text-sm">Password Reset Email Sent!</h4>
                  <p class="text-green-600 text-sm mt-1">Check your inbox for the password reset email.</p>
                  <p class="text-green-600 text-sm mt-1 font-medium">Follow the link in the email to reset your password.</p>
                </div>
              </div>
            </div>

            <!-- Error State in Modal -->
            <div v-if="authStore.error && showForgotPasswordModal" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div class="flex">
                  <UIcon name="i-heroicons-exclamation-triangle" class="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 class="text-red-800 font-medium text-sm">Error</h4>
                    <p class="text-red-600 text-sm mt-1">{{ getErrorMessage(authStore.error) }}</p>
                  </div>
                </div>
                <button @click="authStore.error = null" class="text-red-400 hover:text-red-600 cursor-pointer">
                  <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Resend Verification Modal -->
        <div v-if="showResendModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full">
            <div class="text-center mb-6">
              <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <UIcon name="i-heroicons-envelope" class="w-6 h-6 text-orange-600" />
              </div>
              <h3 class="text-2xl font-bold text-gray-900 mb-2">Resend Verification</h3>
              <p class="text-gray-600">Enter your email and password to resend the verification email.</p>
            </div>

            <form @submit.prevent="handleResendVerification" class="space-y-4">
              <div>
                <label for="resend-email" class="block text-sm font-medium text-gray-700 mb-2">
                  Email address
                </label>
                <input
                  id="resend-email"
                  v-model="resendForm.email"
                  type="email"
                  required
                  :disabled="authStore.loading"
                  placeholder="Enter your email address"
                  class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>

              <div>
                <label for="resend-password" class="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  id="resend-password"
                  v-model="resendForm.password"
                  type="password"
                  required
                  :disabled="authStore.loading"
                  placeholder="Enter your password"
                  class="w-full px-4 py-3 border border-orange-200 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400 disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>

              <div class="flex space-x-3 pt-4">
                <button
                  type="button"
                  @click="() => { 
                    trackButtonClick('Cancel Resend Verification', {}); 
                    showResendModal = false; 
                    resendForm.email = ''; 
                    resendForm.password = ''; 
                  }"
                  :disabled="authStore.loading"
                  class="flex-1 px-4 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="!resendForm.email || !resendForm.password || authStore.loading"
                  class="flex-1 px-4 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 focus:outline-none focus:ring-2 focus:ring-orange-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                >
                  <UIcon v-if="authStore.loading" name="i-heroicons-arrow-path" class="w-4 h-4 mr-2 animate-spin" />
                  <span>{{ authStore.loading ? 'Sending...' : 'Resend Email' }}</span>
                </button>
              </div>
            </form>

            <!-- Success State in Modal -->
            <div v-if="resendVerificationSent" class="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
              <div class="flex">
                <UIcon name="i-heroicons-check-circle" class="w-5 h-5 text-green-400 mr-2 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 class="text-green-800 font-medium text-sm">Verification Email Sent!</h4>
                  <p class="text-green-600 text-sm mt-1">Check your inbox for the verification email.</p>
                </div>
              </div>
            </div>

            <!-- Error State in Modal -->
            <div v-if="authStore.error && showResendModal" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div class="flex">
                  <UIcon name="i-heroicons-exclamation-triangle" class="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 class="text-red-800 font-medium text-sm">Error</h4>
                    <p class="text-red-600 text-sm mt-1">{{ getErrorMessage(authStore.error) }}</p>
                  </div>
                </div>
                <button @click="authStore.error = null" class="text-red-400 hover:text-red-600 cursor-pointer">
                  <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '~/stores/auth'
  import { useAdobeTracking } from '~/composables/useAdobeTracking'
  
  const authStore = useAuthStore()
  
  // Adobe Tracking
const { trackButtonClick, trackError } = useAdobeTracking()
  
  // State
  const activeTab = ref('login')
  const logoError = ref(false)
  const showPassword = ref(false)
  const rememberMe = ref(false)
  const acceptTerms = ref(true)
  const showSuccess = ref(false)
  const showForgotPasswordModal = ref(false)
  const passwordResetSent = ref(false)
  const forgotPasswordEmail = ref('')
  const showResendModal = ref(false)
  const successMessage = ref('')
  const resendVerificationSent = ref(false)

  
  // Form data
  const loginForm = ref({
    email: '',
    password: ''
  })
  
  const registerForm = ref({
    email: '',
    password: '',
    confirmPassword: ''
  })

  const resendForm = ref({
    email: '',
    password: ''
  })
  
  // Computed
  const isLoginFormValid = computed(() => {
    return loginForm.value.email.length > 0 && loginForm.value.password.length > 0
  })
  
  // Configure allowed email domains via NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS env var
  // e.g. NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS="yourcompany.com,partner.com"
  // Leave empty to allow any email domain
  const isValidEmail = computed(() => {
    const allowedDomains = (useRuntimeConfig().public.allowedEmailDomains as string || '').split(',').filter(Boolean)
    if (allowedDomains.length === 0) return true
    return allowedDomains.some(domain => registerForm.value.email.endsWith(`@${domain.trim()}`))
  })
  
  const isRegisterFormValid = computed(() => {
    return registerForm.value.email.length > 0 &&
           isValidEmail.value &&
           registerForm.value.password.length >= 6 && 
           registerForm.value.password === registerForm.value.confirmPassword &&
           acceptTerms.value
  })
  
  const isDevelopment = computed(() => {
    if (typeof window === 'undefined') return false
    const hostname = window.location.hostname
    return hostname === 'localhost' || hostname === '127.0.0.1' || hostname.includes('.local')
  })
  
  // Methods
  const handleLogin = async () => {
    try {
      isManualLogin.value = true
      
      await authStore.login(loginForm.value.email, loginForm.value.password)
      
      // Set flag to indicate successful login for welcome modal
      sessionStorage.setItem('just_logged_in', 'true')
      
      // Clear any previous registration success message for normal login
      successMessage.value = ''
      showSuccess.value = true
      
      // Immediate redirect for better UX
      await navigateTo('/')
    } catch (error) {
      console.error('Login failed:', error)
      isManualLogin.value = false // Reset flag on error
      
      // Track login error
      trackError('auth_login_failed', getErrorMessage(error.message || error.toString()), {
        emailDomain: loginForm.value.email.split('@')[1] || 'unknown',
        hasRememberMe: rememberMe.value,
        formValid: isLoginFormValid.value,
        errorCode: error.code || 'unknown',
        authMethod: 'email_password'
      })
    }
  }
  
  const handleRegister = async () => {
    // Email domain validation (configure allowed domains via NUXT_PUBLIC_ALLOWED_EMAIL_DOMAINS)
    if (!isValidEmail.value) {
      authStore.error = 'Registration is restricted to authorized email domains only.'
      
      // Track email domain validation error
      trackError('auth_registration_invalid_domain', 'Registration attempted with non-authorized email domain', {
        emailDomain: registerForm.value.email.split('@')[1] || 'unknown',
        formValid: isRegisterFormValid.value,
        passwordLength: registerForm.value.password.length,
        acceptedTerms: acceptTerms.value
      })
      
      return
    }
  
    try {
      const result = await authStore.register(registerForm.value.email, registerForm.value.password, { 
        sendVerificationEmail: true 
      })
      
      if (result.success) {
        // Show success message and switch to login tab
        showSuccess.value = true
        activeTab.value = 'login'
        
        // Clear registration form
        registerForm.value = { email: '', password: '', confirmPassword: '' }
        acceptTerms.value = true
        
        // Handle verification requirement based on environment
        if (result.requiresVerification) {
          // Production: Show verification message
          successMessage.value = 'Registration successful! Please check your email and verify your account before logging in. Don\'t forget to check your spam folder if you don\'t see the email.'
        } else {
          // Development: Direct login or Production fallback
          successMessage.value = result.message || 'Registration successful! You are now logged in.'
          
          // Set flag to indicate successful registration/login for welcome modal
          sessionStorage.setItem('just_registered', 'true')
          
          // Set manual flag to prevent double redirect
          isManualLogin.value = true
          
          // Immediate redirect for better UX
          await navigateTo('/')
        }
      }
    } catch (error) {
      console.error('Registration failed:', error)
      
      // Track registration error
      trackError('auth_registration_failed', getErrorMessage(error.message || error.toString()), {
        emailDomain: registerForm.value.email.split('@')[1] || 'unknown',
        passwordLength: registerForm.value.password.length,
        acceptedTerms: acceptTerms.value,
        formValid: isRegisterFormValid.value,
        errorCode: error.code || 'unknown',
        authMethod: 'email_password'
      })
    }
  }
  
  const handleForgotPassword = async () => {
    try {
      await authStore.resetPassword(forgotPasswordEmail.value)
      passwordResetSent.value = true
      setTimeout(() => {
        closeForgotPasswordModal()
      }, 3000) // Auto-close after 3 seconds
    } catch (error) {
      console.error('Password reset failed:', error)
      
      // Track password reset error
      trackError('auth_password_reset_failed', getErrorMessage(error.message || error.toString()), {
        emailDomain: forgotPasswordEmail.value.split('@')[1] || 'unknown',
        hasValidEmail: !!forgotPasswordEmail.value.trim(),
        errorCode: error.code || 'unknown',
        resetMethod: 'email'
      })
    }
  }

  const closeForgotPasswordModal = () => {
    showForgotPasswordModal.value = false
    passwordResetSent.value = false
    forgotPasswordEmail.value = ''
    authStore.error = null
  }

  const handleResendVerification = async () => {
    try {
      // Track resend verification attempt
      trackButtonClick('Resend Verification Submit', {
        emailDomain: resendForm.value.email.split('@')[1] || 'unknown',
        hasValidEmail: !!resendForm.value.email.trim(),
        hasPassword: !!resendForm.value.password.trim()
      })
      
      await authStore.resendVerificationEmail(resendForm.value.email, resendForm.value.password)
      resendVerificationSent.value = true
      setTimeout(() => {
        showResendModal.value = false
        resendVerificationSent.value = false
        resendForm.value.email = ''
        resendForm.value.password = ''
        authStore.error = null
      }, 3000) // Auto-close after 3 seconds
    } catch (error) {
      console.error('Resend verification failed:', error)
      
      // Track resend verification error
      trackError('auth_resend_verification_failed', getErrorMessage(error.message || error.toString()), {
        emailDomain: resendForm.value.email.split('@')[1] || 'unknown',
        hasValidEmail: !!resendForm.value.email.trim(),
        hasPassword: !!resendForm.value.password.trim(),
        errorCode: error.code || 'unknown',
        resendMethod: 'email_password'
      })
    }
  }

  const getErrorMessage = (error) => {
    const errorMap = {
      'auth/user-not-found': 'No account found with this email address.',
      'auth/wrong-password': 'Incorrect password. Please try again.',
      'auth/email-already-in-use': 'An account with this email already exists.',
      'auth/weak-password': 'Password should be at least 6 characters.',
      'auth/invalid-email': 'Please enter a valid email address.',
      'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
      'auth/missing-email': 'Please enter your email address.',
      'auth/invalid-continue-uri': 'Invalid continue URL provided.',
      'auth/unauthorized-continue-uri': 'Domain not authorized for password reset. Please contact your system administrator.',
      'Domain not authorized for password reset': 'The email domain is not authorized for password reset. Please contact your system administrator.'
    }
    
    for (const [code, message] of Object.entries(errorMap)) {
      if (error.includes(code)) {
        return message
      }
    }
    
    return error
  }
  
  // Redirect if already authenticated
  onMounted(async () => {
    await authStore.init()
    if (authStore.isAuthenticated) {
      await navigateTo('/')
    }
  })
  
  // State for manual login to prevent double redirects
  const isManualLogin = ref(false)
  
  // Watch for authentication changes (only for auto-navigation, not manual login)
  watch(() => authStore.isAuthenticated, async (isAuth) => {
    if (isAuth && authStore.user && !isManualLogin.value) {
      // Only auto-redirect if this wasn't triggered by our manual login
      await navigateTo('/')
    } else if (isAuth && isManualLogin.value) {
      // Reset flag after successful manual login
      isManualLogin.value = false
    }
  })
  
  // SEO
useHead({
  title: 'Login - DAISY',
  meta: [
    { name: 'description', content: 'Sign in to your DAISY account to access AI-powered assistants and components.' }
  ]
})
  </script>