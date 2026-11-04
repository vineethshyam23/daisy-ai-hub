<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50">
    <!-- Header wird automatisch durch das default layout angezeigt -->
    <UContainer class="py-16">
      <div class="max-w-4xl mx-auto">
        <!-- Page Title -->
        <div class="text-center mb-12">
          <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-500 to-amber-500 bg-clip-text text-transparent mb-4">
            Terms of Service
          </h1>
          <p class="text-xl text-gray-600">
            Last updated: January 2025
          </p>
        </div>

        <!-- Content -->
        <div class="bg-white/70 backdrop-blur-sm rounded-3xl border border-orange-100 shadow-xl p-8 md:p-12">
          <div class="prose prose-lg max-w-none">
            
            <!-- Introduction -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">1. Introduction</h2>
            <p class="text-gray-600 mb-8">
              Welcome to AI Hub. These Terms of Service ("Terms") govern your use of our AI-powered assistants and services. By accessing or using our services, you agree to be bound by these Terms.
            </p>

            <!-- Acceptance of Terms -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">2. Acceptance of Terms</h2>
            <p class="text-gray-600 mb-8">
              By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
            </p>

            <!-- Use License -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">3. Use License</h2>
            <p class="text-gray-600 mb-4">
              Permission is granted to temporarily access and use the materials on DAISY for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
            </p>
            <ul class="list-disc pl-6 text-gray-600 mb-8">
              <li>modify or copy the materials</li>
              <li>use the materials for any commercial purpose or for any public display</li>
              <li>attempt to reverse engineer any software contained on the website</li>
              <li>remove any copyright or other proprietary notations from the materials</li>
            </ul>

            <!-- User Accounts -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">4. User Accounts</h2>
            <p class="text-gray-600 mb-8">
              When you create an account with us, you must provide information that is accurate, complete, and current at all times. You are responsible for safeguarding the password and for all activities that occur under your account.
            </p>

            <!-- AI Services -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">5. AI Services and Content</h2>
            <p class="text-gray-600 mb-8">
              Our AI-powered assistants are provided "as is" and we make no warranties about the accuracy, reliability, or suitability of the generated content. Users are responsible for reviewing and validating any AI-generated content before use.
            </p>

            <!-- Privacy -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">6. Privacy and Data Protection</h2>
            <p class="text-gray-600 mb-8">
              Your privacy is important to us. Our collection and use of personal information is governed by our Privacy Policy, which is incorporated into these Terms by reference.
            </p>

            <!-- Prohibited Uses -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">7. Prohibited Uses</h2>
            <p class="text-gray-600 mb-4">
              You may not use our service:
            </p>
            <ul class="list-disc pl-6 text-gray-600 mb-8">
              <li>For any unlawful purpose or to solicit others to perform unlawful acts</li>
              <li>To violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances</li>
              <li>To infringe upon or violate our intellectual property rights or the intellectual property rights of others</li>
              <li>To harass, abuse, insult, harm, defame, slander, disparage, intimidate, or discriminate</li>
              <li>To submit false or misleading information</li>
            </ul>

            <!-- Termination -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">8. Termination</h2>
            <p class="text-gray-600 mb-8">
              We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
            </p>

            <!-- Limitation of Liability -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">9. Limitation of Liability</h2>
            <p class="text-gray-600 mb-8">
              In no event shall the service provider, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses.
            </p>

            <!-- Governing Law -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">10. Governing Law</h2>
            <p class="text-gray-600 mb-8">
              These Terms shall be interpreted and governed by the laws of Germany, without regard to its conflict of law provisions. Our failure to enforce any right or provision of these Terms will not be considered a waiver of those rights.
            </p>

            <!-- Changes to Terms -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">11. Changes to Terms of Service</h2>
            <p class="text-gray-600 mb-8">
              We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days notice prior to any new terms taking effect.
            </p>

            <!-- Contact Information -->
            <h2 class="text-2xl font-bold text-gray-800 mb-6">12. Contact Information</h2>
            <p class="text-gray-600 mb-4">
              If you have any questions about these Terms of Service, please contact the Legal Team:
            </p>
            <div class="bg-gray-50 rounded-lg p-6 mb-8">
              <p class="text-gray-700 font-medium">Your Company Name</p>
              <p class="text-gray-600">Legal Team<br>Email:
                <a href="mailto:legal@yourcompany.com">legal@yourcompany.com</a></p>
            </div>

          </div>
        </div>

        <!-- Back to Home Button -->
        <div class="text-center mt-12">
          <UButton
            @click="$router.push('/')"
            size="lg"
            class="bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg hover:from-orange-600 hover:to-amber-600 hover:shadow-xl transition-all"
          >
            <UIcon name="i-heroicons-arrow-left" class="w-5 h-5 mr-2" />
            Back to Home
          </UButton>
        </div>
      </div>
    </UContainer>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Terms of Service - DAISY',
  meta: [
    { 
      name: 'description', 
      content: 'Terms of Service for AI Hub platform.'
    }
  ]
})
</script> 