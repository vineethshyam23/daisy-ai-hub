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
        <p class="text-gray-600 font-light">Loading your workspace...</p>
        <div class="mt-4 flex justify-center">
          <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    </div>

  <!-- Main Content - Only show if authenticated -->
  <div v-else-if="authStore.isAuthenticated" class="min-h-screen bg-gradient-to-br from-orange-50 via-orange-25 to-amber-50">
    <!-- Unified Header -->
    <AIHeader />

    <!-- Main Content -->
    <UContainer>
      <!-- Access Denied Message for Search Features -->
      <div v-if="showAccessDeniedMessage" class="mt-8 mb-6">
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start space-x-3">
          <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
          <div class="flex-1">
            <h4 class="text-amber-800 font-medium text-sm mb-1">Feature Access Notice</h4>
            <p class="text-amber-700 text-sm">
              Search features are not available for your organization. You have full access to all AI assistants below.
            </p>
          </div>
          <button 
            @click="showAccessDeniedMessage = false"
            class="text-amber-600 hover:text-amber-800 text-sm font-medium"
          >
            <UIcon name="i-heroicons-x-mark" class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Search & Support Section -->
      <div v-if="canAccessSearchSupport" class="mt-8 mb-8">
        <div class="relative bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl overflow-hidden">
          <!-- AI Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <svg class="w-full h-full" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="search-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                  <circle cx="10" cy="10" r="1" fill="white"/>
                  <path d="M5,5 L15,15 M15,5 L5,15" stroke="white" stroke-width="0.5"/>
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#search-pattern)"/>
            </svg>
          </div>
          
          <!-- Neural Network Background -->
          <div class="absolute inset-0 opacity-5">
            <div class="w-full h-full" style="background-image: radial-gradient(circle at 25% 25%, white 2px, transparent 2px), radial-gradient(circle at 75% 75%, white 2px, transparent 2px); background-size: 50px 50px, 30px 30px;"></div>
          </div>
          
          <div class="relative z-10 p-8 md:p-12">
            <div class="mb-8">
              <h2 class="text-2xl font-bold text-white mb-2">
                Search & Support
              </h2>
              <p class="text-white/90 font-light">Find information for selected topics, pages, and get support for your questions.</p>
            </div>
            
            <!-- Search Categories -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <!-- Welcome Search -->
              <NuxtLink 
                to="/search/welcome"
                @click="trackButtonClick('Navigate to Search Widget', { searchType: 'welcome', navigationType: 'search_category' })"
                class="group bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/20 hover:border-white/40 transition-all cursor-pointer"
              >
                <div class="flex items-center space-x-4 mb-3">
                  <div class="flex-shrink-0 w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                    <UIcon name="i-heroicons-home" class="w-6 h-6 text-white" />
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-white mb-1">Welcome</h3>
                    <p class="text-white/80 text-sm">Search onboarding guides and getting started resources</p>
                  </div>
                </div>
              </NuxtLink>

              <!-- IT Support Search -->
              <NuxtLink 
                to="/search/support"
                @click="trackButtonClick('Navigate to Search Widget', { searchType: 'support', navigationType: 'search_category' })"
                class="group bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/20 hover:border-white/40 transition-all cursor-pointer"
              >
                <div class="flex items-center space-x-4 mb-3">
                  <div class="flex-shrink-0 w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                    <UIcon name="i-heroicons-wrench-screwdriver" class="w-6 h-6 text-white" />
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-white mb-1">IT Support</h3>
                    <p class="text-white/80 text-sm">Find technical support and troubleshooting guides</p>
                  </div>
                </div>
              </NuxtLink>

              <!-- Legal Search -->
              <NuxtLink 
                to="/search/legal"
                @click="trackButtonClick('Navigate to Search Widget', { searchType: 'legal', navigationType: 'search_category' })"
                class="group bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/20 hover:border-white/40 transition-all cursor-pointer"
              >
                <div class="flex items-center space-x-4 mb-3">
                  <div class="flex-shrink-0 w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                    <UIcon name="i-heroicons-scale" class="w-6 h-6 text-white" />
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-white mb-1">Legal Resources</h3>
                    <p class="text-white/80 text-sm">Search legal documents and compliance guides</p>
                  </div>
                </div>
              </NuxtLink>

              <!-- Information Security Search -->
              <NuxtLink 
                to="/search/security"
                @click="trackButtonClick('Navigate to Search Widget', { searchType: 'security', navigationType: 'search_category' })"
                class="group bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-6 hover:bg-white/20 hover:border-white/40 transition-all cursor-pointer"
              >
                <div class="flex items-center space-x-4 mb-3">
                  <div class="flex-shrink-0 w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                    <UIcon name="i-heroicons-shield-check" class="w-6 h-6 text-white" />
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-white mb-1">Information Security</h3>
                    <p class="text-white/80 text-sm">Search security policies and best practices</p>
                  </div>
                </div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>



      <!-- Filter und View Controls -->
      <div class="mb-8 bg-gradient-to-br from-stone-500 via-stone-400 to-stone-300 backdrop-blur-sm rounded-2xl shadow-xl p-6">
        <div class="flex flex-col lg:flex-row gap-6 items-start lg:items-center justify-between mb-6">
          <!-- Suchfeld -->
          <div class="flex-1 max-w-md">
            <input
              v-model="aiHub.searchQuery"
              type="text"
              placeholder="Which assistant are you looking for?"
              class="w-full px-4 py-3 text-lg bg-stone-600 border-2 border-stone-400 text-stone-100 placeholder-stone-300 rounded-lg focus:border-stone-300 focus:outline-none transition-colors"
            />
          </div>
        </div>

        <!-- Kategorie Filter -->
        <div class="flex flex-wrap gap-3">
          <button
            v-for="category in aiHub.categories"
            :key="category.id"
            @click="() => { 
              trackButtonClick('Filter by Category', { 
                categoryId: category.id, 
                categoryName: category.name,
                previousCategory: aiHub.selectedCategory,
                totalComponents: aiHub.components.length
              }); 
              aiHub.setSelectedCategory(category.id); 
            }"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer',
              aiHub.selectedCategory === category.id 
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white' 
                : 'bg-stone-600 text-stone-100 hover:bg-stone-500 border border-stone-400'
            ]"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- All Components Section -->
      <div class="mb-12">
        <div class="flex items-center justify-between mb-12">
          <div>
            <h3 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-2">
              {{ aiHub.searchQuery || aiHub.selectedCategory !== 'all' ? 'Search Results' : 'All Assistants' }}
            </h3>
            <p class="text-lg text-gray-600 font-light">
              {{ aiHub.filteredComponents.length }} {{ aiHub.filteredComponents.length === 1 ? 'assistant found' : 'assistants found' }}
            </p>
          </div>
          
          <!-- View Toggle -->
          <div class="flex items-center space-x-3">
            <div class="flex rounded-lg shadow-lg overflow-hidden border border-orange-200">
              <button
                @click="() => { 
                  trackButtonClick('Change View Mode', { 
                    newViewMode: 'grid',
                    previousViewMode: aiHub.viewMode,
                    filteredComponentsCount: aiHub.filteredComponents.length
                  }); 
                  aiHub.setViewMode('grid'); 
                }"
                :class="[
                  'flex items-center space-x-2 px-4 py-2 text-sm font-medium transition-all cursor-pointer',
                  aiHub.viewMode === 'grid' 
                    ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white' 
                    : 'bg-white text-gray-600 hover:bg-orange-50'
                ]"
              >
                <UIcon name="i-heroicons-squares-2x2" class="w-4 h-4" />
                <span>Grid</span>
              </button>
              <button
                @click="() => { 
                  trackButtonClick('Change View Mode', { 
                    newViewMode: 'list',
                    previousViewMode: aiHub.viewMode,
                    filteredComponentsCount: aiHub.filteredComponents.length
                  }); 
                  aiHub.setViewMode('list'); 
                }"
                :class="[
                  'flex items-center space-x-2 px-4 py-2 text-sm font-medium transition-all border-l border-orange-200 cursor-pointer',
                  aiHub.viewMode === 'list' 
                    ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white' 
                    : 'bg-white text-gray-600 hover:bg-orange-50'
                ]"
              >
                <UIcon name="i-heroicons-list-bullet" class="w-4 h-4" />
                <span>List</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Grid View -->
        <div v-if="aiHub.viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          <ComponentCard
            v-for="component in aiHub.filteredComponents"
            :key="component.id"
            :component="component"
          />
        </div>

        <!-- List View -->
        <div v-else class="space-y-6">
          <ComponentListItem
            v-for="component in aiHub.filteredComponents"
            :key="component.id"
            :component="component"
          />
        </div>

        <!-- Empty State -->
        <div v-if="aiHub.filteredComponents.length === 0" class="text-center py-20 bg-white/90 backdrop-blur-sm rounded-xl shadow-lg border border-orange-100">
          <div class="w-24 h-24 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <span class="text-4xl">🔍</span>
          </div>
                      <h3 class="text-2xl font-bold text-gray-900 mb-4">No assistants found</h3>
          <p class="text-lg text-gray-600 font-light mb-8 max-w-md mx-auto">
            Try a different search term or select another category.
          </p>
          <button
            @click="() => { 
              trackButtonClick('Clear Search and Filters', { 
                previousSearchQuery: aiHub.searchQuery,
                previousCategory: aiHub.selectedCategory,
                viewMode: aiHub.viewMode
              }); 
              aiHub.setSearchQuery(''); 
              aiHub.setSelectedCategory('all'); 
            }"
            class="px-6 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 hover:shadow-xl transition-all cursor-pointer"
          >
                          Show all assistants
          </button>
        </div>
      </div>

             <!-- Quote of the Day - Small & Subtle -->
       <div v-if="quote" class="mt-12 mb-8">
         <div class="max-w-sm ml-auto bg-gradient-to-br from-gray-700 to-gray-800 border border-gray-600 rounded-xl shadow-lg p-4 hover:shadow-xl transition-shadow">
           <div class="text-center">
             <div class="flex items-center justify-center space-x-1 mb-2">
               <p class="text-gray-300 text-xs font-medium uppercase tracking-wide">Quote of the Day</p>
             </div>
             
             <blockquote class="text-sm text-gray-100 leading-relaxed mb-2 italic font-light">
               "{{ quote.q }}"
             </blockquote>
             
             <p class="text-xs text-gray-400 font-medium">
               — {{ quote.a }}
             </p>
           </div>
         </div>
       </div>

    </UContainer>

    <!-- Welcome Modal -->
    <div v-if="showWelcomeModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-2 sm:p-4" @click="() => { 
      trackButtonClick('Close Welcome Modal', { 
        modalDisplayTime: Date.now() - (modalShowTime.value || Date.now()),
        buttonType: 'outside_click',
        userEmail: authStore.user?.email?.split('@')[1] || 'unknown'
      }); 
      closeWelcomeModal(); 
    }">
      <div class="relative w-full max-w-sm sm:max-w-lg md:max-w-2xl lg:max-w-4xl mx-auto max-h-[95vh] sm:max-h-[90vh]" @click.stop>
        <!-- Close Button - Better mobile positioning -->
        <button
          @click="() => { 
            trackButtonClick('Close Welcome Modal', { 
              modalDisplayTime: Date.now() - (modalShowTime.value || Date.now()),
              buttonType: 'close_button',
              userEmail: authStore.user?.email?.split('@')[1] || 'unknown'
            }); 
            closeWelcomeModal(); 
          }"
          class="absolute -top-2 -right-2 sm:-top-4 sm:-right-4 z-20 w-10 h-10 sm:w-12 sm:h-12 bg-white rounded-full flex items-center justify-center text-gray-600 hover:text-gray-800 hover:bg-gray-50 transition-all shadow-lg hover:shadow-xl cursor-pointer"
        >
          <UIcon name="i-heroicons-x-mark" class="w-5 h-5 sm:w-6 sm:h-6" />
        </button>
        
        <!-- Modal Content -->
        <div class="relative min-h-[70vh] sm:h-[85vh] max-h-[90vh] sm:max-h-[800px] sm:min-h-[600px] rounded-2xl sm:rounded-3xl shadow-2xl overflow-hidden overflow-y-auto">
          <!-- Background Image -->
          <div class="absolute inset-0 bg-gradient-to-br from-blue-900/90 via-purple-900/90 to-pink-900/90">
            <!-- Futuristic AI Workspace Illustration -->
            <div class="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20"></div>
            
            <!-- Geometric AI Pattern Overlay -->
            <div class="absolute inset-0 opacity-20">
              <svg class="w-full h-full" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
                <!-- Neural Network Nodes -->
                <circle cx="50" cy="50" r="3" fill="white" opacity="0.8"/>
                <circle cx="150" cy="80" r="4" fill="white" opacity="0.6"/>
                <circle cx="250" cy="60" r="3" fill="white" opacity="0.9"/>
                <circle cx="350" cy="90" r="2" fill="white" opacity="0.7"/>
                <circle cx="80" cy="150" r="3" fill="white" opacity="0.8"/>
                <circle cx="180" cy="180" r="4" fill="white" opacity="0.6"/>
                <circle cx="280" cy="160" r="3" fill="white" opacity="0.9"/>
                <circle cx="320" cy="200" r="2" fill="white" opacity="0.7"/>
                <circle cx="100" cy="250" r="3" fill="white" opacity="0.8"/>
                <circle cx="200" cy="280" r="4" fill="white" opacity="0.6"/>
                <circle cx="300" cy="260" r="3" fill="white" opacity="0.9"/>
                
                <!-- Connection Lines -->
                <line x1="50" y1="50" x2="150" y2="80" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="150" y1="80" x2="250" y2="60" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="250" y1="60" x2="350" y2="90" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="80" y1="150" x2="180" y2="180" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="180" y1="180" x2="280" y2="160" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="280" y1="160" x2="320" y2="200" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="100" y1="250" x2="200" y2="280" stroke="white" stroke-width="1" opacity="0.3"/>
                <line x1="200" y1="280" x2="300" y2="260" stroke="white" stroke-width="1" opacity="0.3"/>
                
                <!-- Vertical connections -->
                <line x1="50" y1="50" x2="80" y2="150" stroke="white" stroke-width="1" opacity="0.2"/>
                <line x1="150" y1="80" x2="180" y2="180" stroke="white" stroke-width="1" opacity="0.2"/>
                <line x1="250" y1="60" x2="280" y2="160" stroke="white" stroke-width="1" opacity="0.2"/>
                <line x1="180" y1="180" x2="200" y2="280" stroke="white" stroke-width="1" opacity="0.2"/>
              </svg>
            </div>
            
            <!-- Abstract Tech Elements -->
            <div class="absolute top-10 right-10 w-32 h-32 opacity-10">
              <div class="w-full h-full border-2 border-white rounded-lg transform rotate-12"></div>
              <div class="absolute top-2 left-2 w-8 h-8 bg-white rounded-full opacity-60"></div>
              <div class="absolute bottom-4 right-4 w-12 h-2 bg-white rounded-full opacity-40"></div>
            </div>
            
            <div class="absolute bottom-20 left-10 w-24 h-24 opacity-10">
              <div class="w-full h-full border border-white rounded-full"></div>
              <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-white rounded-full opacity-80"></div>
            </div>
          </div>
          
          <!-- Content Overlay -->
          <div class="relative z-10 h-full flex flex-col justify-start pt-6 sm:pt-8 md:pt-12 pb-6 sm:pb-8 md:pb-12 px-4 sm:px-8 md:px-12 lg:px-16 xl:px-20">
            <div class="text-center max-w-4xl mx-auto flex-1 flex flex-col justify-center">
              <div class="mb-4 sm:mb-6">
                <div class="inline-flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16 bg-white/10 backdrop-blur-sm rounded-2xl sm:rounded-3xl mb-4 sm:mb-6 border border-white/20">
                  <UIcon name="i-heroicons-document-magnifying-glass" class="w-6 h-6 sm:w-8 sm:h-8 text-white" />
                </div>
              </div>
              
              <h2 class="text-xl sm:text-2xl md:text-3xl lg:text-5xl font-bold text-white mb-3 sm:mb-4 leading-tight">
                🆕 Introducing
                <span class="block bg-gradient-to-r from-orange-400 via-amber-400 to-yellow-400 bg-clip-text text-transparent">
                  Document Processor
                </span>
                <span class="block text-white text-lg sm:text-xl md:text-2xl lg:text-4xl">AI-Powered Document Processing</span>
              </h2>
              
              <p class="text-sm sm:text-base md:text-lg lg:text-xl text-white/90 font-light mb-3 sm:mb-4 max-w-3xl mx-auto leading-relaxed px-2 sm:px-0">
                Upload PDFs, images, and documents to extract text with advanced OCR and AI. Apply complex processing operations like data transformation, format conversion, and intelligent content analysis with custom instructions.
              </p>
              
              <div class="bg-white/10 backdrop-blur-sm rounded-xl sm:rounded-2xl p-3 sm:p-4 mb-4 sm:mb-6 max-w-2xl mx-auto border border-white/20">
                <div class="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-4 text-xs sm:text-sm">
                  <div class="flex items-center space-x-2">
                    <UIcon name="i-heroicons-check-circle" class="w-4 h-4 sm:w-5 sm:h-5 text-green-400" />
                    <span class="text-white font-medium">Only 1 Token per use</span>
                  </div>
                  <div class="hidden sm:block w-px h-4 bg-white/30"></div>
                  <div class="flex items-center space-x-2">
                    <UIcon name="i-heroicons-sparkles" class="w-4 h-4 sm:w-5 sm:h-5 text-yellow-400" />
                    <span class="text-white font-medium">Smart Instructions</span>
                  </div>
                  <div class="hidden sm:block w-px h-4 bg-white/30"></div>
                  <div class="flex items-center space-x-2">
                    <UIcon name="i-heroicons-arrow-down-tray" class="w-4 h-4 sm:w-5 sm:h-5 text-blue-400" />
                    <span class="text-white font-medium">PDF Export</span>
                  </div>
                </div>
              </div>
              
              <div class="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-3 mb-6 sm:mb-8 md:mb-12">
                <div class="flex items-center space-x-2 px-3 sm:px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
                  <UIcon name="i-heroicons-document-magnifying-glass" class="w-3 h-3 sm:w-4 sm:h-4 text-orange-400" />
                  <span class="text-white text-xs sm:text-sm font-medium">Smart OCR</span>
                </div>
                <div class="flex items-center space-x-2 px-3 sm:px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
                  <UIcon name="i-heroicons-adjustments-horizontal" class="w-3 h-3 sm:w-4 sm:h-4 text-blue-400" />
                  <span class="text-white text-xs sm:text-sm font-medium">Complex Operations</span>
                </div>
                <div class="flex items-center space-x-2 px-3 sm:px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
                  <UIcon name="i-heroicons-language" class="w-3 h-3 sm:w-4 sm:h-4 text-green-400" />
                  <span class="text-white text-xs sm:text-sm font-medium">Multi-Format Support</span>
                </div>
              </div>
              
              <!-- Try Document Processor Button -->
              <div class="flex justify-center mb-4">
                <button
                  @click="() => { 
                    trackButtonClick(`Welcome Modal Try Document Processor`, { 
                      modalDisplayTime: Date.now() - (modalShowTime.value || Date.now()),
                      buttonType: 'try_document_processor',
                      userEmail: authStore.user?.email?.split('@')[1] || 'unknown'
                    }); 
                    closeWelcomeModal();
                    navigateTo('/ai/document-processor');
                  }"
                  class="inline-flex items-center px-4 sm:px-6 py-3 sm:py-4 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-bold text-sm sm:text-base rounded-lg sm:rounded-xl shadow-2xl hover:from-orange-600 hover:to-amber-600 transform hover:scale-105 transition-all duration-300 cursor-pointer"
                >
                  <UIcon name="i-heroicons-document-magnifying-glass" class="w-5 h-5 sm:w-6 sm:h-6 mr-2 sm:mr-3" />
                  <span class="whitespace-nowrap">Try Document Processor Now!</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAIHubStore } from '~/stores/aiHub'
import { useAuthStore } from '~/stores/auth'
import { useTokenStore } from '~/stores/tokens'
import { useRoleStore } from '~/stores/roles'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

// Stores
const aiHub = useAIHubStore()
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const roleStore = useRoleStore()

// Adobe Tracking
const { trackButtonClick, trackError } = useAdobeTracking()

// State
const showWelcomeModal = ref(false)
const showAccessDeniedMessage = ref(false)

// Quote state
const quote = ref(null)

// Access control for Search & Support section
const canAccessSearchSupport = computed(() => {
  return !!authStore.user?.email
})

// Helper methods for dynamic component styling
const getComponentClasses = (color) => {
  const colorMap = {
    purple: 'bg-gray-100 border-purple-200 hover:bg-gray-50 hover:border-purple-300',
    indigo: 'bg-gray-100 border-indigo-200 hover:bg-gray-50 hover:border-indigo-300',
    pink: 'bg-gray-100 border-pink-200 hover:bg-gray-50 hover:border-pink-300',
    blue: 'bg-gray-100 border-blue-200 hover:bg-gray-50 hover:border-blue-300',
    cyan: 'bg-gray-100 border-cyan-200 hover:bg-gray-50 hover:border-cyan-300',
    teal: 'bg-gray-100 border-teal-200 hover:bg-gray-50 hover:border-teal-300',
    orange: 'bg-gray-100 border-orange-200 hover:bg-gray-50 hover:border-orange-300',
    green: 'bg-gray-100 border-green-200 hover:bg-gray-50 hover:border-green-300'
  }
  return colorMap[color] || 'bg-gray-100 border-gray-200 hover:bg-gray-50 hover:border-gray-300'
}

const getIconClasses = (color) => {
  const colorMap = {
    purple: 'bg-gradient-to-br from-purple-500 to-pink-500 shadow-md',
    indigo: 'bg-gradient-to-br from-indigo-500 to-purple-500 shadow-md',
    pink: 'bg-gradient-to-br from-pink-500 to-rose-500 shadow-md',
    blue: 'bg-gradient-to-br from-blue-500 to-cyan-500 shadow-md',
    cyan: 'bg-gradient-to-br from-cyan-500 to-blue-500 shadow-md',
    teal: 'bg-gradient-to-br from-teal-500 to-emerald-500 shadow-md',
    orange: 'bg-gradient-to-br from-orange-500 to-amber-500 shadow-md',
    green: 'bg-gradient-to-br from-green-500 to-emerald-500 shadow-md'
  }
  return colorMap[color] || 'bg-gradient-to-br from-gray-500 to-slate-500 shadow-md'
}

const getHoverTextClasses = (color) => {
  const colorMap = {
    purple: 'group-hover:text-purple-600',
    indigo: 'group-hover:text-indigo-600',
    pink: 'group-hover:text-pink-600',
    blue: 'group-hover:text-blue-600',
    cyan: 'group-hover:text-cyan-600',
    teal: 'group-hover:text-teal-600',
    orange: 'group-hover:text-orange-600',
    green: 'group-hover:text-green-600'
  }
  return colorMap[color] || 'group-hover:text-gray-600'
}

// Welcome Modal functions
const closeWelcomeModal = () => {
  showWelcomeModal.value = false
  
  // Clear ALL welcome-related flags to prevent re-showing
  if (authStore.user?.uid) {
    sessionStorage.removeItem(`welcome_modal_pending_${authStore.user.uid}`)
  }
  
  // Also clear the just_logged_in flag if it still exists
  sessionStorage.removeItem('just_logged_in')
}

const shouldShowWelcomeModal = () => {
  // Only show modal if there's a pending welcome flag from login
  if (!authStore.user?.uid) {
    return false
  }
  
  const hasPendingWelcome = sessionStorage.getItem(`welcome_modal_pending_${authStore.user.uid}`)
  
  return hasPendingWelcome === 'true'
}

// Function to mark that welcome modal should be shown (called after login)
const markWelcomeModalPending = () => {
  if (authStore.user?.uid) {
    sessionStorage.setItem(`welcome_modal_pending_${authStore.user.uid}`, 'true')
  }
}

// Track when modal is shown
const modalShowTime = ref(null)

// Quote functionality with session caching
const getQuoteStorageKey = () => {
  const today = new Date().toDateString()
  return `quote_of_the_day_${today}`
}

const loadCachedQuote = () => {
  try {
    const storageKey = getQuoteStorageKey()
    const cachedQuote = sessionStorage.getItem(storageKey)
    
    if (cachedQuote) {
      const parsedQuote = JSON.parse(cachedQuote)
      quote.value = parsedQuote
      return true
    }
  } catch (error) {
    console.error('Error loading cached quote:', error)
  }
  return false
}

const fetchQuoteInBackground = async () => {
  // Don't fetch if we already have a quote for today
  if (quote.value) return
  
  try {
    // Use our Nuxt API route as proxy (no CORS issues)
    const response = await $fetch('/api/inspirational-quote')
    
    if (response && response.quote) {
      // Transform the response to match our quote structure
      const newQuote = {
        q: response.quote.text,
        a: response.quote.author
      }
      
      // Save to session storage for the day
      try {
        const storageKey = getQuoteStorageKey()
        sessionStorage.setItem(storageKey, JSON.stringify(newQuote))
        
        // Clean up old quotes from previous days
        cleanupOldQuotes()
      } catch (storageError) {
        console.warn('Could not save quote to session storage:', storageError)
      }
      
      // Update the quote (this will make the component appear)
      quote.value = newQuote
      
      // Track if we're using fallback quotes
      if (response.fallback) {
        console.warn('Using fallback quote due to ZenQuotes API issue:', response.error)
      }
    } else {
      throw new Error('No quote data received from API')
    }
    
  } catch (error) {
    console.error('Error fetching quote in background:', error)
    
    // Track quote fetch error but don't show to user
    trackError('quote_fetch_failed_background', 'Failed to fetch quote of the day in background', {
      errorMessage: error.message || error.toString(),
      errorType: error.name || 'unknown',
      apiUrl: '/api/inspirational-quote',
      currentPage: 'index'
    })
  }
}

const cleanupOldQuotes = () => {
  try {
    const today = new Date().toDateString()
    const keysToRemove = []
    
    // Find old quote keys
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i)
      if (key && key.startsWith('quote_of_the_day_') && !key.includes(today)) {
        keysToRemove.push(key)
      }
    }
    
    // Remove old quotes
    keysToRemove.forEach(key => {
      sessionStorage.removeItem(key)
    })
    
  } catch (error) {
    console.error('Error cleaning up old quotes:', error)
  }
}

// Handle ESC key to close modal
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && showWelcomeModal.value) {
    trackButtonClick('Close Welcome Modal', {
      modalDisplayTime: Date.now() - (modalShowTime.value || Date.now()),
      buttonType: 'escape_key',
      userEmail: authStore.user?.email?.split('@')[1] || 'unknown'
    })
    closeWelcomeModal()
  }
}

// Client-side auth check and redirect
onMounted(async () => {
  // Add escape key listener
  document.addEventListener('keydown', handleEscapeKey)
  try {

    
    // Check if user just logged in (reliable flag set during login)
    const justLoggedIn = sessionStorage.getItem('just_logged_in') === 'true'
    
    // Wait for DOM to be fully ready
    await nextTick()
    
    // Wait for auth store to be initialized (by the plugin)
    // Don't call authStore.init() again to avoid race conditions
    if (!authStore.isInitialized) {
      let attempts = 0
      while (!authStore.isInitialized && attempts < 100) {
        await new Promise(resolve => setTimeout(resolve, 100))
        attempts++
      }
      
      if (!authStore.isInitialized) {
        console.warn('Auth store initialization timeout, redirecting to login')
        
        // Track auth initialization timeout error
        trackError('auth_init_timeout', 'Authentication store initialization timeout after 10 seconds', {
          attempts: attempts,
          maxAttempts: 100,
          timeoutSeconds: 10,
          redirectTo: 'login'
        })
        
        await navigateTo('/login')
        return
      }
    }
    
    // Check authentication after initialization
    if (!authStore.isAuthenticated) {
      await navigateTo('/login')
      return
    }

    // Only mark welcome modal as pending if user ACTUALLY just logged in
    if (justLoggedIn && authStore.user?.uid) {
      markWelcomeModalPending()
      sessionStorage.removeItem('just_logged_in') // Clean up the flag immediately
    }

    // Check for search access denied redirect
    const route = useRoute()
    if (route.query.error === 'search_access_denied') {
      showAccessDeniedMessage.value = true
      
      // Clear the error query parameter from URL
      await navigateTo('/', { replace: true })
    }

    // Initialize AI Hub store to load custom order
    if (!aiHub.isOrderLoaded) {
      try {
        await aiHub.init()
      } catch (error) {
        console.error('Error initializing AI Hub store:', error)
        
        // Track AI Hub store initialization error
        trackError('store_init_aihub_failed', 'Failed to initialize AI Hub store on index page', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user
        })
      }
    }

    // Initialize role store after auth (with error handling)
    if (authStore.isAuthenticated && authStore.user && !roleStore.isInitialized) {
      try {
        await roleStore.init()
      } catch (error) {
        console.error('Error initializing role store:', error)
        
        // Track role store initialization error
        trackError('store_init_role_failed', 'Failed to initialize role store on index page', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user
        })
      }
    }

    // Initialize token store after auth (with error handling)
    if (authStore.isAuthenticated && authStore.user && !tokenStore.isInitialized) {
      try {
        await tokenStore.init()
      } catch (error) {
        console.error('Error initializing token store:', error)
        
        // Track token store initialization error
        trackError('store_init_token_failed', 'Failed to initialize token store on index page', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user
        })
      }
    }

    // Only show welcome modal if there's a pending flag from actual login
    if (shouldShowWelcomeModal()) {
      modalShowTime.value = Date.now()
      showWelcomeModal.value = true
    }

    // Load quote of the day (cached first, then background fetch)
    const hadCachedQuote = loadCachedQuote()
    
    if (!hadCachedQuote) {
      // Fetch in background without blocking page load
      fetchQuoteInBackground()
    }

  } catch (error) {
    console.error('Error in onMounted:', error)
    
    // Track general initialization error
    trackError('page_init_failed', 'Critical error during index page initialization', {
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      isAuthenticated: authStore.isAuthenticated,
      hasUser: !!authStore.user,
      authInitialized: authStore.isInitialized,
      continuingWithLimitedFunctionality: true
    })
    
    // Don't automatically redirect on error, let user decide
    console.warn('Continuing with limited functionality')
  }
})

// Watch for auth state changes
watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
  if (!isAuthenticated) {
    await navigateTo('/login')
  } else if (authStore.user) {
    // Initialize role store when user logs in
    if (!roleStore.isInitialized) {
      try {
        await roleStore.init()
      } catch (error) {
        console.error('Error initializing role store after auth change:', error)
        
        // Track role store initialization error after auth change
        trackError('store_init_role_failed_auth_change', 'Failed to initialize role store after authentication change', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user,
          trigger: 'auth_state_change'
        })
      }
    }
    
    // Initialize token store when user logs in
    if (!tokenStore.isInitialized) {
      try {
        await tokenStore.init()
      } catch (error) {
        console.error('Error initializing token store after auth change:', error)
        
        // Track token store initialization error after auth change
        trackError('store_init_token_failed_auth_change', 'Failed to initialize token store after authentication change', {
          errorMessage: error.message || error.toString(),
          errorCode: error.code || 'unknown',
          userId: authStore.user?.uid || 'unknown',
          isAuthenticated: authStore.isAuthenticated,
          hasUser: !!authStore.user,
          trigger: 'auth_state_change'
        })
      }
    }
    
    // Only show welcome modal if there's a pending flag from actual login
    // (Note: This watch hook is mainly for auth state changes, not for showing welcome modal)
    if (shouldShowWelcomeModal()) {
      modalShowTime.value = Date.now()
      showWelcomeModal.value = true
    }
  }
})

// Watch for role store initialization to force reactivity
watch(() => roleStore.isInitialized, (isInitialized) => {
  if (isInitialized) {
    // Force reactivity update by accessing the computed property
    nextTick(() => {
      // Just trigger reactivity, no logging needed
      aiHub.filteredComponents.length
    })
  }
})

// Cleanup event listeners
onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
})

// SEO
useHead({
  title: 'DAISY - AI-powered Assistants and Components',
  meta: [
    {
      name: 'description',
      content: 'Discover our collection of AI-powered assistants and components for more productive work. Get your daily inspiration with our quote of the day.'
    }
  ]
})
</script>