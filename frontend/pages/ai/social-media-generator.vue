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
      <p class="text-gray-600 font-light">Loading Social Media Generator...</p>
      <div class="mt-4 flex justify-center">
        <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-pink-50 via-pink-25 to-rose-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-r from-pink-800 via-pink-600 to-pink-500 border-b border-pink-700 overflow-hidden">
      <!-- Social Media Pattern -->
      <div class="absolute right-0 top-0 w-1/2 h-full opacity-8">
        <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="social-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="2" fill="none" stroke="white" stroke-width="0.5"/>
              <path d="M6,6 L14,14 M14,6 L6,14" stroke="white" stroke-width="0.3"/>
              <circle cx="10" cy="10" r="0.5" fill="white"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#social-pattern)"/>
        </svg>
      </div>
      
      <!-- Social Network Background -->
      <div class="absolute right-0 top-0 w-2/3 h-full opacity-4">
        <div class="w-full h-full" style="background-image: radial-gradient(circle at 85% 20%, white 2px, transparent 2px), radial-gradient(circle at 75% 80%, white 1.5px, transparent 1.5px), radial-gradient(circle at 90% 50%, white 1px, transparent 1px); background-size: 35px 35px, 25px 25px, 50px 50px;"></div>
      </div>
      
      <UContainer class="relative z-10 py-16">
        <div class="max-w-4xl">
          <div class="flex items-center mb-6">
            <div class="w-16 h-16 bg-pink-500 rounded-2xl flex items-center justify-center mr-6 border border-pink-700">
              <UIcon name="i-heroicons-hashtag" class="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 class="text-4xl font-bold text-white mb-2">Social Media Post Generator</h1>
              <p class="text-xl text-pink-100">Create engaging social media content with AI creativity</p>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <UContainer class="py-8">
      
      <!-- Content Configuration Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Content Input -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <div class="flex items-center space-x-3 mb-6">
            <UIcon name="i-heroicons-pencil-square" class="w-6 h-6 text-pink-600" />
            <h2 class="text-2xl font-bold text-gray-900">Content Input</h2>
          </div>
          
          <div class="space-y-4">
            <!-- Topic/Theme -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Topic or Theme</label>
              <input
                v-model="contentInput.topic"
                type="text"
                placeholder="What's your post about? (e.g., new product launch, company news...)"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg"
              />
            </div>
            
            <!-- Key Message -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Key Message</label>
              <textarea
                v-model="contentInput.message"
                placeholder="Describe the main message or content you want to share..."
                rows="4"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg resize-y min-h-[100px]"
              ></textarea>
            </div>
            
            <!-- Target Audience -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Target Audience</label>
              <input
                v-model="contentInput.audience"
                type="text"
                placeholder="Who is this for? (e.g., professionals, young adults, customers...)"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg"
              />
            </div>
            
            <!-- Call to Action -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Call to Action (Optional)</label>
              <input
                v-model="contentInput.cta"
                type="text"
                placeholder="What should people do? (e.g., visit website, buy now, comment...)"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg"
              />
            </div>
          </div>
        </div>

        <!-- Platform & Style Settings -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <div class="flex items-center space-x-3 mb-6">
            <UIcon name="i-heroicons-adjustments-horizontal" class="w-6 h-6 text-pink-600" />
            <h2 class="text-2xl font-bold text-gray-900">Platform & Style</h2>
          </div>
          
          <div class="space-y-4">
            <!-- Platform Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Platform</label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="platform in platforms"
                  :key="platform.value"
                  @click="postSettings.platform = platform.value"
                                      :class="[
                    'p-3 rounded-lg border transition-all text-sm font-medium cursor-pointer',
                    postSettings.platform === platform.value
                      ? 'border-pink-500 bg-pink-50 text-pink-700'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-pink-300'
                  ]"
                >
                  <div class="flex items-center space-x-2">
                    <UIcon :name="platform.icon" class="w-4 h-4" />
                    <span>{{ platform.label }}</span>
                  </div>
                </button>
              </div>
            </div>
            
            <!-- Tone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tone</label>
              <select
                v-model="postSettings.tone"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="professional">Professional - Business tone</option>
                <option value="casual">Casual - Relaxed and friendly</option>
                <option value="enthusiastic">Enthusiastic - Excited and energetic</option>
                <option value="friendly">Friendly - Warm and approachable</option>
                <option value="inspiring">Inspiring - Motivational and uplifting</option>
                <option value="humorous">Humorous - Fun and entertaining</option>
              </select>
            </div>
            
            <!-- Content Style -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Content Style</label>
              <select
                v-model="postSettings.style"
                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors text-lg cursor-pointer"
              >
                <option value="informative">Informative - Educational content</option>
                <option value="storytelling">Storytelling - Narrative approach</option>
                <option value="question">Question-based - Engage with questions</option>
                <option value="list">List/Tips - Structured information</option>
                <option value="bts">Behind-the-scenes - Insider view</option>
                <option value="announcement">Announcement - News and updates</option>
              </select>
            </div>
            
            <!-- Include Hashtags -->
            <div class="flex items-center space-x-3">
              <div class="relative">
                <input
                  type="checkbox"
                  id="include-hashtags"
                  v-model="postSettings.includeHashtags"
                  class="sr-only"
                />
                <div 
                  @click="postSettings.includeHashtags = !postSettings.includeHashtags"
                  class="w-5 h-5 bg-white border border-gray-300 rounded cursor-pointer flex items-center justify-center transition-all duration-200 hover:border-pink-400"
                  :class="postSettings.includeHashtags ? 'border-pink-500 bg-white' : ''"
                >
                  <UIcon 
                    v-if="postSettings.includeHashtags" 
                    name="i-heroicons-check" 
                    class="w-4 h-4 text-pink-600 font-bold"
                  />
                </div>
              </div>
              <label for="include-hashtags" class="text-sm font-medium text-gray-700 cursor-pointer">
                Include relevant hashtags
              </label>
            </div>
            
            <!-- Include Emojis -->
            <div class="flex items-center space-x-3">
              <div class="relative">
                <input
                  type="checkbox"
                  id="include-emojis"
                  v-model="postSettings.includeEmojis"
                  class="sr-only"
                />
                <div 
                  @click="postSettings.includeEmojis = !postSettings.includeEmojis"
                  class="w-5 h-5 bg-white border border-gray-300 rounded cursor-pointer flex items-center justify-center transition-all duration-200 hover:border-pink-400"
                  :class="postSettings.includeEmojis ? 'border-pink-500 bg-white' : ''"
                >
                  <UIcon 
                    v-if="postSettings.includeEmojis" 
                    name="i-heroicons-check" 
                    class="w-4 h-4 text-pink-600 font-bold"
                  />
                </div>
              </div>
              <label for="include-emojis" class="text-sm font-medium text-gray-700 cursor-pointer">
                Include emojis
              </label>
            </div>
            
            <!-- Generate Image -->
            <div class="flex items-center space-x-3">
              <div class="relative">
                <input
                  type="checkbox"
                  id="generate-image"
                  v-model="postSettings.generateImage"
                  class="sr-only"
                />
                <div 
                  @click="postSettings.generateImage = !postSettings.generateImage"
                  class="w-5 h-5 bg-white border border-gray-300 rounded cursor-pointer flex items-center justify-center transition-all duration-200 hover:border-pink-400"
                  :class="postSettings.generateImage ? 'border-pink-500 bg-white' : ''"
                >
                  <UIcon 
                    v-if="postSettings.generateImage" 
                    name="i-heroicons-check" 
                    class="w-4 h-4 text-pink-600 font-bold"
                  />
                </div>
              </div>
              <label for="generate-image" class="text-sm font-medium text-gray-700 cursor-pointer">
                Generate image for post
              </label>
            </div>
            
            <!-- Generate Button -->
            <div class="pt-4">
              <UButton 
                @click="generatePost"
                :loading="isGenerating"
                :disabled="tokenStore.isTokenDataReady && !tokenStore.hasTokensForAssistant('social-media-generator')"
                color="primary"
                size="xl"
                :class="[
                  'w-full font-semibold transition-all duration-300',
                  (!tokenStore.isTokenDataReady || tokenStore.hasTokensForAssistant('social-media-generator'))
                    ? 'bg-pink-600 hover:bg-pink-700 text-white cursor-pointer' 
                    : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                ]"
                icon="i-heroicons-sparkles"
              >
                <span v-if="isGenerating">Creating Post...</span>
                <span v-else-if="!tokenStore.isTokenDataReady">Loading tokens...</span>
                <span v-else-if="!tokenStore.hasTokensForAssistant('social-media-generator')">
                  Insufficient Tokens ({{ tokenStore.getTokenCost('social-media-generator') }} required)
                </span>
                <span v-else>
                  Generate Post ({{ tokenStore.getTokenCost('social-media-generator') }} token)
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
        disclaimer-text="This content is created using AI and may require adjustments to align with our brand values and communication goals. Please review before publishing."
        class="mb-6"
      />

      <!-- Modern Loading State -->
      <div v-if="isGenerating" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="text-center py-12">
          <div class="flex justify-center mb-6">
            <div class="relative">
              <div class="animate-spin rounded-full h-20 w-20 border-4 border-pink-200 border-t-pink-600"></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <UIcon name="i-heroicons-megaphone" class="text-2xl text-pink-600" />
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-center space-x-2 mb-2">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-pink-600" />
            <h3 class="text-2xl font-bold text-gray-900">Creating Your Social Media Post</h3>
          </div>
          <p class="text-gray-600 mb-8">Crafting the perfect content for your audience...</p>
          
          <!-- Progress Animation -->
          <div class="max-w-md mx-auto">
            <div class="bg-pink-100 rounded-full h-3">
              <div 
                class="bg-pink-600 h-3 rounded-full transition-all duration-500" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <div class="flex items-center justify-center space-x-2 mt-4">
              <UIcon name="i-heroicons-cpu-chip" class="text-sm text-pink-500" />
              <p class="text-sm text-gray-600 font-medium">{{ progressText }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Generated Posts Section -->
      <div v-if="generatedPosts.length > 0" class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8 mb-8">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-megaphone" class="w-6 h-6 text-pink-600" />
            <h2 class="text-2xl font-bold text-gray-900">Generated Posts</h2>
          </div>
          <div class="flex space-x-2">
            <button
              @click="generateMore"
              :disabled="isGeneratingMore || (tokenStore.isTokenDataReady && !tokenStore.hasTokensForAssistant('social-media-generator'))"
              :class="[
                'font-medium px-4 py-2 flex items-center space-x-2 border transition-all duration-200 hover:shadow-md rounded-lg',
                isGeneratingMore || (tokenStore.isTokenDataReady && !tokenStore.hasTokensForAssistant('social-media-generator'))
                  ? 'border-gray-300 bg-gray-100 text-gray-500 cursor-not-allowed'
                  : 'border-gray-300 hover:border-pink-400 hover:bg-pink-50 hover:text-pink-600 cursor-pointer'
              ]"
            >
              <UIcon 
                :name="isGeneratingMore ? 'i-heroicons-arrow-path' : 'i-heroicons-plus'" 
                class="w-5 h-5" 
                :class="{ 'animate-spin': isGeneratingMore }"
              />
              <span>{{ isGeneratingMore ? 'Generating...' : 'Generate More' }}</span>
            </button>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="(post, index) in generatedPosts"
            :key="index"
            class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm"
          >
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-pink-100 flex items-center justify-center">
                  <UIcon :name="getPlatformIcon(postSettings.platform)" class="w-6 h-6 text-pink-600" />
                </div>
                <span class="font-semibold text-gray-800 text-lg">{{ getPlatformName(postSettings.platform) }}</span>
              </div>
              <div class="flex space-x-3">
                <div class="relative">
                  <UButton
                    @click="copyPost(post)"
                    size="lg"
                    variant="outline"
                    class="cursor-pointer font-medium px-4 py-2 flex items-center space-x-2 border border-gray-300 hover:border-blue-400 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200 hover:shadow-md"
                  >
                    <UIcon name="i-heroicons-clipboard-document" class="w-5 h-5" />
                    <span>Copy</span>
                  </UButton>
                  <!-- Copy Confirmation Text -->
                  <div v-if="copyConfirmations[index]" class="absolute top-full mt-2 left-0 z-50 text-sm text-green-600 font-medium flex items-center space-x-1 whitespace-nowrap bg-white px-3 py-2 rounded-lg shadow-lg border border-green-200">
                    <UIcon name="i-heroicons-check-circle" class="w-4 h-4" />
                    <span>Post copied to clipboard!</span>
                  </div>
                </div>
                <UButton
                  @click="editPost(index)"
                  size="lg"
                  variant="outline"
                  :class="[
                    'cursor-pointer font-medium px-4 py-2 flex items-center space-x-2 border transition-all duration-200',
                    editingPostIndex === index 
                      ? 'border-pink-500 bg-pink-50 text-pink-700 hover:border-pink-600 hover:bg-pink-100'
                      : 'border-gray-300 hover:border-pink-400 hover:bg-pink-50 hover:text-pink-600'
                  ]"
                >
                  <UIcon :name="editingPostIndex === index ? 'i-heroicons-check' : 'i-heroicons-pencil'" class="w-5 h-5" />
                  <span>{{ editingPostIndex === index ? 'Save' : 'Edit' }}</span>
                </UButton>
              </div>
            </div>
            
            <!-- Generated Image (if available) -->
            <div v-if="post.image" class="mb-4 relative group">
              <img 
                :src="post.image" 
                alt="Generated image for social media post"
                class="w-full rounded-lg border border-gray-200 shadow-sm cursor-pointer transition-transform duration-200 hover:scale-[1.02]"
                @click="openImageModal(post.image)"
              />
              
              <!-- Image Hover Overlay -->
              <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex items-center justify-center">
                <div class="flex space-x-3">
                  <button
                    @click.stop="openImageModal(post.image)"
                    class="flex items-center space-x-2 px-4 py-2 bg-white/90 hover:bg-white text-gray-900 font-medium rounded-lg shadow-lg transition-all duration-200 cursor-pointer"
                  >
                    <UIcon name="i-heroicons-eye" class="w-4 h-4" />
                    <span class="text-sm">View</span>
                  </button>
                  <button
                    @click.stop="downloadImageFromPost(post.image, index)"
                    class="flex items-center space-x-2 px-4 py-2 bg-black/70 hover:bg-black/80 text-white font-medium rounded-lg shadow-lg transition-all duration-200 cursor-pointer"
                  >
                    <UIcon name="i-heroicons-arrow-down-tray" class="w-4 h-4" />
                    <span class="text-sm">Download</span>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Post Content -->
            <div class="bg-gray-50 rounded-lg p-4">
              <!-- Editing Mode -->
              <div v-if="editingPostIndex === index" class="space-y-3">
                <textarea
                  v-model="editingPostContent"
                  rows="8"
                  class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none resize-y min-h-[150px] font-sans text-gray-800 text-sm leading-relaxed"
                  placeholder="Edit your post content..."
                ></textarea>
                <div class="flex justify-between items-center">
                  <span class="text-xs text-gray-500">{{ editingPostContent.length }} characters</span>
                  <div class="flex space-x-2">
                    <button
                      @click="cancelEdit"
                      class="px-3 py-1.5 text-gray-600 hover:text-gray-800 font-medium text-sm transition-colors cursor-pointer"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
              <!-- Display Mode -->
              <div v-else>
                <pre class="whitespace-pre-wrap font-sans text-gray-800 text-sm leading-relaxed">{{ post.content }}</pre>
              </div>
            </div>
            
            <!-- Character Count (Display Mode) -->
            <div v-if="editingPostIndex !== index" class="mt-3 text-xs text-gray-500 text-right">
              {{ post.content.length }} characters
            </div>
          </div>
        </div>
      </div>

      <!-- Platform Guidelines -->
      <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
        <div class="flex items-center space-x-3 mb-6">
          <UIcon name="i-heroicons-information-circle" class="w-6 h-6 text-pink-600" />
          <h3 class="text-xl font-bold text-gray-900">Platform Guidelines</h3>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="guide in platformGuidelines" :key="guide.platform" class="space-y-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-lg bg-pink-100 flex items-center justify-center">
                <UIcon :name="guide.icon" class="w-5 h-5 text-pink-600" />
              </div>
              <h4 class="font-semibold text-gray-800">{{ guide.platform }}</h4>
            </div>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• Length: {{ guide.length }}</li>
              <li>• Best time: {{ guide.bestTime }}</li>
              <li>• Style: {{ guide.style }}</li>
            </ul>
          </div>
        </div>
      </div>
    </UContainer>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="fixed inset-0 bg-black/75 flex items-center justify-center p-4 z-50" @click="showImageModal = false">
      <div class="bg-white rounded-2xl max-w-4xl max-h-[90vh] overflow-auto border border-gray-200 shadow-2xl" @click.stop>
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <UIcon name="i-heroicons-photo" class="text-2xl text-pink-600" />
            <h3 class="text-xl font-bold text-gray-900">Social Media Image</h3>
          </div>
          <button 
            @click="showImageModal = false" 
            class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer"
          >
            <UIcon name="i-heroicons-x-mark" class="w-6 h-6" />
          </button>
        </div>
        
        <div class="p-6">
          <div v-if="selectedImage" class="text-center">
            <img 
              :src="selectedImage.url" 
              alt="Generated social media image" 
              class="max-w-full max-h-[60vh] object-contain rounded-lg shadow-lg mx-auto"
            />
          </div>
        </div>
        
        <div class="flex justify-between items-center p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <div class="flex items-center space-x-2 text-gray-600">
            <UIcon name="i-heroicons-information-circle" class="w-5 h-5" />
            <span class="text-sm">Click outside to close or use the download button</span>
          </div>
          <button 
            @click="downloadImageFromModal" 
            class="flex items-center space-x-2 px-6 py-3 bg-pink-600 hover:bg-pink-700 text-white font-medium rounded-xl transition-all duration-200 cursor-pointer"
          >
            <UIcon name="i-heroicons-arrow-down-tray" class="w-5 h-5" />
            <span>Download Image</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tips Section -->
    <UContainer class="py-8">
      <div class="border border-pink-200 rounded-2xl shadow-sm p-8" style="background-color: rgba(236, 72, 153, 0.25);">
        <div class="flex items-center space-x-2 mb-4">
          <UIcon name="i-heroicons-light-bulb" class="text-2xl text-pink-800" />
          <h3 class="text-xl font-bold text-pink-900">Tips for Better Results</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h4 class="font-semibold text-pink-800">Content Strategy</h4>
            <ul class="text-sm text-pink-700 space-y-1">
              <li>• Be specific about your target audience</li>
              <li>• Include key messages or call-to-actions</li>
              <li>• Mention trending topics or seasonal relevance</li>
            </ul>
          </div>
          <div class="space-y-3">
            <h4 class="font-semibold text-pink-800">Platform Optimization</h4>
            <ul class="text-sm text-pink-700 space-y-1">
              <li>• Choose the right platform for your content type</li>
              <li>• Consider character limits and best practices</li>
              <li>• Use engaging formats like lists or questions</li>
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
const contentInput = ref({
  topic: '',
  message: '',
  audience: '',
  cta: ''
})

const postSettings = ref({
  platform: 'linkedin',
  tone: 'professional',
  style: 'informative',
  includeHashtags: true,
  includeEmojis: true,
  generateImage: true
})

const generatedPosts = ref([]) // Each item will be {content: string, image?: string}
const isGenerating = ref(false)
const editingPostIndex = ref(-1) // Track which post is being edited
const editingPostContent = ref('') // Store the content being edited
const showImageModal = ref(false)
const selectedImage = ref(null)
const progress = ref(0)
const progressText = ref('')
const copyConfirmations = ref([]) // Track copy confirmations for each post
const isGeneratingMore = ref(false) // Track loading state for "Generate More" button

// Platform Options
const platforms = [
  { label: 'LinkedIn', value: 'linkedin', icon: 'i-heroicons-briefcase' },
  { label: 'Twitter/X', value: 'twitter', icon: 'i-heroicons-at-symbol' },
  { label: 'Facebook', value: 'facebook', icon: 'i-heroicons-users' },
  { label: 'Instagram', value: 'instagram', icon: 'i-heroicons-camera' }
]

// Native HTML form elements are now used instead of USelect/UInput for better compatibility

// Platform Guidelines
const platformGuidelines = [
  {
    platform: 'LinkedIn',
    icon: 'i-heroicons-briefcase',
    length: '1,300 chars',
    bestTime: '8-10 AM',
    style: 'Professional, insights'
  },
  {
    platform: 'Twitter/X',
    icon: 'i-heroicons-at-symbol',
    length: '280 chars',
    bestTime: '9 AM, 1-3 PM',
    style: 'Concise, trending'
  },
  {
    platform: 'Facebook',
    icon: 'i-heroicons-users',
    length: '40-80 chars',
    bestTime: '1-4 PM',
    style: 'Personal, engaging'
  },
  {
    platform: 'Instagram',
    icon: 'i-heroicons-camera',
    length: '10-50 chars',
    bestTime: '11 AM-1 PM',
    style: 'Visual, lifestyle'
  }
]

// Methods
const generatePost = async () => {
  if (!contentInput.value.topic.trim() || !contentInput.value.message.trim()) {
    const toast = useToast()
    toast.add({
      title: 'Missing Information',
      description: 'Please fill in both topic and key message fields.',
      color: 'yellow',
      timeout: 5000
    })
    return
  }

  // Check if user has sufficient tokens
  if (!tokenStore.hasTokensForAssistant('social-media-generator')) {
    const toast = useToast()
    toast.add({
      title: 'Insufficient Tokens',
      description: `You need ${tokenStore.getTokenCost('social-media-generator')} token(s) to use this assistant. Your tokens will reset in ${tokenStore.getHoursUntilReset()} hours.`,
      color: 'red',
      timeout: 8000
    })
    return
  }

  // Track button click with structured data
  trackButtonClick('Generate Social Media Post', {
    platform: postSettings.value.platform,
    tone: postSettings.value.tone,
    style: postSettings.value.style,
    includeHashtags: postSettings.value.includeHashtags,
    includeEmojis: postSettings.value.includeEmojis,
    generateImage: postSettings.value.generateImage,
    hasAudience: !!contentInput.value.audience.trim(),
    hasCTA: !!contentInput.value.cta.trim(),
    topicLength: contentInput.value.topic.length,
    messageLength: contentInput.value.message.length
  })

  isGenerating.value = true
  progress.value = 0
  
  try {
    // Simulate progress
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 15
        updateProgressText()
      }
    }, 800)

    // Clear progress when done
    const clearProgress = () => {
      clearInterval(progressInterval)
      progress.value = 100
      progressText.value = 'Complete!'
      setTimeout(() => {
        progress.value = 0
        progressText.value = ''
      }, 2000)
    }
    // Prepare API payload
    const payload = {
      topic: contentInput.value.topic,
      key_message: contentInput.value.message,
      target_audience: contentInput.value.audience || 'General audience',
      call_to_action: contentInput.value.cta || '',
      platform: postSettings.value.platform.charAt(0).toUpperCase() + postSettings.value.platform.slice(1),
      tone: postSettings.value.tone.charAt(0).toUpperCase() + postSettings.value.tone.slice(1),
      content_style: postSettings.value.style.charAt(0).toUpperCase() + postSettings.value.style.slice(1),
      include_hashtags: postSettings.value.includeHashtags,
      include_emojis: postSettings.value.includeEmojis,
      generate_image: postSettings.value.generateImage
    }

    // Call the authenticated API
    const { authenticatedApiRequestNative } = await import('~/config/api.config')
    const response = await authenticatedApiRequestNative('/social-media/post', {
      method: 'POST',
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    
    // Extract content and clean up HTML
    let generatedContent = data.content
    if (generatedContent) {
      // Remove HTML tags and decode content
      generatedContent = generatedContent
        .replace(/```html\n/g, '')
        .replace(/```/g, '')
        .replace(/<p>/g, '')
        .replace(/<\/p>/g, '\n')
        .replace(/\n\n\n/g, '\n\n')
        .trim()
    }
    
    // Create post object with content and optional image
    const postObject = {
      content: generatedContent,
      image: data.image || null
    }
    
    // Add the generated post
    generatedPosts.value = [postObject]
    
    // Complete progress animation
    clearProgress()
    
    // Consume token after successful generation - use the simpler useTokens method
    const tokenCost = tokenStore.getTokenCost('social-media-generator')
    const tokenConsumed = await tokenStore.useTokens(tokenCost)
    
    if (tokenConsumed) {
      // Track token usage
      const { trackTokenUsage } = useAdobeTracking()
      trackTokenUsage(tokenCost, 'social_media_generator', {
        platform: postSettings.value.platform,
        tone: postSettings.value.tone,
        style: postSettings.value.style,
        includeHashtags: postSettings.value.includeHashtags,
        includeEmojis: postSettings.value.includeEmojis,
        generateImage: postSettings.value.generateImage,
        topicLength: contentInput.value.topic.length,
        messageLength: contentInput.value.message.length
      })
    } else {
      console.warn('Failed to consume tokens, but response was successful')
    }
    
    // Show success notification
    const toast = useToast()
    toast.add({
      title: 'Post Generated!',
      description: 'Your social media post has been created successfully.',
      color: 'green',
      timeout: 5000
    })
    
  } catch (error) {
    // Clear progress on error
    clearInterval(progressInterval)
    progress.value = 0
    progressText.value = ''
    console.error('Error generating posts:', error)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_social_media_generator_failed', 'Social Media Generator API request failed', {
      errorMessage: error.message || error.toString(),
      errorCode: error.status || error.statusCode || 'unknown',
      errorType: error.name || 'APIError',
      endpoint: 'socialMediaPost',
      requestData: {
        platform: postSettings.value.platform,
        tone: postSettings.value.tone,
        style: postSettings.value.style,
        includeHashtags: postSettings.value.includeHashtags,
        includeEmojis: postSettings.value.includeEmojis,
        generateImage: postSettings.value.generateImage,
        topicLength: contentInput.value.topic.length,
        messageLength: contentInput.value.message.length,
        hasAudience: !!contentInput.value.audience.trim(),
        hasCTA: !!contentInput.value.cta.trim()
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    const toast = useToast()
    toast.add({
      title: 'Generation Error',
      description: 'Failed to generate social media post. Please try again.',
      color: 'red',
      timeout: 5000
    })
  } finally {
    isGenerating.value = false
  }
}

const generateMockPost = (variant) => {
  const platform = postSettings.value.platform
  const topic = contentInput.value.topic
  const message = contentInput.value.message
  const hashtags = postSettings.value.includeHashtags ? '\n\n#innovation #technology #business' : ''
  const emojis = postSettings.value.includeEmojis ? '🚀 ' : ''
  
  if (platform === 'linkedin') {
    return `${emojis}${topic} - A Game Changer!

${message}

This represents a significant step forward in our industry. Here's what makes it special:

✅ Innovation at its finest
✅ User-focused approach  
✅ Scalable solution

What are your thoughts on this development? I'd love to hear your perspective in the comments!${hashtags}`
  } else if (platform === 'twitter') {
    return `${emojis}Big news: ${topic}!

${message.substring(0, 100)}...

This changes everything! 🔥${hashtags}`
  } else if (platform === 'facebook') {
    return `${emojis}Exciting update about ${topic}!

${message}

We're thrilled to share this with our community. What do you think?${hashtags}`
  } else {
    return `${emojis}${topic} ✨

${message}

Swipe to see more details! 👉${hashtags}`
  }
}

const generateMore = async () => {
  if (!tokenStore.hasTokensForAssistant('social-media-generator')) {
    const toast = useToast()
    toast.add({
      title: 'Insufficient Tokens',
      description: `You need ${tokenStore.getTokenCost('social-media-generator')} token(s) to generate more posts.`,
      color: 'red',
      timeout: 5000
    })
    return
  }

  isGeneratingMore.value = true

  try {
    // Prepare API payload with slight variation for different content
    const payload = {
      topic: contentInput.value.topic,
      key_message: contentInput.value.message + ' Here\'s another perspective:',
      target_audience: contentInput.value.audience || 'General audience',
      call_to_action: contentInput.value.cta || '',
      platform: postSettings.value.platform.charAt(0).toUpperCase() + postSettings.value.platform.slice(1),
      tone: postSettings.value.tone.charAt(0).toUpperCase() + postSettings.value.tone.slice(1),
      content_style: postSettings.value.style.charAt(0).toUpperCase() + postSettings.value.style.slice(1),
      include_hashtags: postSettings.value.includeHashtags,
      include_emojis: postSettings.value.includeEmojis,
      generate_image: postSettings.value.generateImage
    }

    // Call the authenticated API
    const { authenticatedApiRequestNative } = await import('~/config/api.config')
    const response = await authenticatedApiRequestNative('/social-media/post', {
      method: 'POST',
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    
    // Extract content and clean up HTML
    let generatedContent = data.content
    if (generatedContent) {
      // Remove HTML tags and decode content
      generatedContent = generatedContent
        .replace(/```html\n/g, '')
        .replace(/```/g, '')
        .replace(/<p>/g, '')
        .replace(/<\/p>/g, '\n')
        .replace(/\n\n\n/g, '\n\n')
        .trim()
    }
    
    // Create post object with content and optional image
    const postObject = {
      content: generatedContent,
      image: data.image || null
    }
    
    // Add the generated post
    generatedPosts.value.push(postObject)
    
    // Consume token after successful generation - use the simpler useTokens method
    const tokenCost = tokenStore.getTokenCost('social-media-generator')
    const tokenConsumed = await tokenStore.useTokens(tokenCost)
    
    if (tokenConsumed) {
      // Track token usage
      const { trackTokenUsage } = useAdobeTracking()
      trackTokenUsage(tokenCost, 'social_media_generator', {
        platform: postSettings.value.platform,
        tone: postSettings.value.tone,
        style: postSettings.value.style,
        includeHashtags: postSettings.value.includeHashtags,
        includeEmojis: postSettings.value.includeEmojis,
        generateImage: postSettings.value.generateImage,
        topicLength: contentInput.value.topic.length,
        messageLength: contentInput.value.message.length,
        isGenerateMore: true
      })
    } else {
      console.warn('Failed to consume tokens, but response was successful')
    }
    
  } catch (error) {
    console.error('Error generating more posts:', error)
    
    // Track API error with Adobe Analytics
    const { trackError } = useAdobeTracking()
    trackError('api_social_media_generator_more_failed', 'Social Media Generator generate more API request failed', {
      errorMessage: error.message || error.toString(),
      errorCode: error.status || error.statusCode || 'unknown',
      errorType: error.name || 'APIError',
      endpoint: 'socialMediaPost',
      action: 'generateMore',
      requestData: {
        platform: postSettings.value.platform,
        tone: postSettings.value.tone,
        style: postSettings.value.style,
        includeHashtags: postSettings.value.includeHashtags,
        includeEmojis: postSettings.value.includeEmojis,
        generateImage: postSettings.value.generateImage,
        topicLength: contentInput.value.topic.length,
        messageLength: contentInput.value.message.length,
        hasAudience: !!contentInput.value.audience.trim(),
        hasCTA: !!contentInput.value.cta.trim(),
        existingPostsCount: generatedPosts.value.length
      },
      userAgent: window.navigator?.userAgent || 'unknown',
      timestamp: new Date().toISOString()
    })
    
    const toast = useToast()
    toast.add({
      title: 'Generation Error',
      description: 'Failed to generate additional posts. Please try again.',
      color: 'red',
      timeout: 5000
    })
  } finally {
    isGeneratingMore.value = false
  }
}

const copyPost = async (post) => {
  try {
    // Track copy action
    const postIndex = generatedPosts.value.findIndex(p => p === post)
    trackButtonClick('Copy Social Media Post', {
      postIndex: postIndex + 1,
      platform: postSettings.value.platform,
      contentLength: post.content.length,
      hasImage: !!post.image
    })

    await navigator.clipboard.writeText(post.content)
    if (postIndex !== -1) {
      // Set confirmation for this specific post
      copyConfirmations.value[postIndex] = true
      // Hide the confirmation after 3 seconds
      setTimeout(() => {
        copyConfirmations.value[postIndex] = false
      }, 3000)
    }
  } catch (error) {
    console.error('Failed to copy:', error)
    const toast = useToast()
    toast.add({
      title: 'Copy Failed',
      description: 'Unable to copy to clipboard. Please try again.',
      color: 'red',
      timeout: 3000
    })
  }
}

const editPost = (index) => {
  if (editingPostIndex.value === index) {
    // Track save edit action
    trackButtonClick('Save Edited Post', {
      postIndex: index + 1,
      platform: postSettings.value.platform,
      originalLength: generatedPosts.value[index].content.length,
      editedLength: editingPostContent.value.length,
      lengthDifference: editingPostContent.value.length - generatedPosts.value[index].content.length
    })

    // Save the edited content
    generatedPosts.value[index].content = editingPostContent.value
    editingPostIndex.value = -1
    editingPostContent.value = ''
    
    const toast = useToast()
    toast.add({
      title: 'Post Updated!',
      description: 'Your changes have been saved.',
      color: 'green',
      timeout: 3000
    })
  } else {
    // Track start edit action
    trackButtonClick('Start Edit Post', {
      postIndex: index + 1,
      platform: postSettings.value.platform,
      contentLength: generatedPosts.value[index].content.length
    })

    // Start editing
    editingPostIndex.value = index
    editingPostContent.value = generatedPosts.value[index].content
  }
}

const cancelEdit = () => {
  editingPostIndex.value = -1
  editingPostContent.value = ''
}

const openImageModal = (imageUrl) => {
  selectedImage.value = { url: imageUrl }
  showImageModal.value = true
}

const downloadImageFromPost = (imageUrl, index) => {
  try {
    // Track image download
    trackButtonClick('Download Social Media Image', {
      postIndex: index + 1,
      platform: postSettings.value.platform,
      downloadSource: 'post_view'
    })

    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `social-media-image-${index + 1}-${Date.now()}.png`
    link.style.display = 'none'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    const toast = useToast()
    toast.add({
      title: 'Download Started',
      description: 'Image download has been started.',
      color: 'green',
      timeout: 3000
    })
  } catch (error) {
    console.error('Download failed:', error)
    // Fallback: open in new tab
    window.open(imageUrl, '_blank')
  }
}

const downloadImageFromModal = () => {
  if (selectedImage.value) {
    try {
      const link = document.createElement('a')
      link.href = selectedImage.value.url
      link.download = `social-media-image-${Date.now()}.png`
      link.style.display = 'none'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      const toast = useToast()
      toast.add({
        title: 'Download Started',
        description: 'Image download has been started.',
        color: 'green',
        timeout: 3000
      })
    } catch (error) {
      console.error('Download failed:', error)
      window.open(selectedImage.value.url, '_blank')
    }
  }
}

const getPlatformIcon = (platform) => {
  const platformMap = {
    linkedin: 'i-heroicons-briefcase',
    twitter: 'i-heroicons-at-symbol',
    facebook: 'i-heroicons-users',
    instagram: 'i-heroicons-camera'
  }
  return platformMap[platform] || 'i-heroicons-device-phone-mobile'
}

const getPlatformName = (platform) => {
  const platformMap = {
    linkedin: 'LinkedIn',
    twitter: 'Twitter/X',
    facebook: 'Facebook',
    instagram: 'Instagram'
  }
  return platformMap[platform] || platform
}

const updateProgressText = () => {
  const texts = [
    'Analyzing your content...',
    'Crafting the perfect tone...',
    'Adding creative elements...',
    'Optimizing for your platform...',
    'Generating hashtags...',
    'Almost ready...'
  ]
  const index = Math.floor((progress.value / 100) * (texts.length - 1))
  progressText.value = texts[index] || texts[0]
}

// SEO
useHead({
  title: 'Social Media Post Generator - DAISY',
  meta: [
    { name: 'description', content: 'Create engaging social media posts for all platforms with AI-powered creativity and optimization.' }
  ]
})
</script> 