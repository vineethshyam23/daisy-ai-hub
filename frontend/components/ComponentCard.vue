<template>
  <div 
    class="group cursor-pointer transition-all duration-500 hover:scale-[1.02] hover:-translate-y-2"
    @click="navigateToComponent"
  >
    <!-- Main Card Container -->
    <div class="relative bg-white rounded-3xl shadow-2xl hover:shadow-3xl overflow-hidden transition-all duration-500" style="border-radius: 1.5rem; overflow: hidden;">
      
      <!-- Gradient Background Overlay -->
      <div class="absolute inset-0 bg-gradient-to-br from-orange-50/30 via-transparent to-purple-50/20 pointer-events-none"></div>
      
      <!-- Badges Container -->
      <div class="absolute top-0 right-0 z-10 flex flex-col space-y-1">
        <!-- Featured Badge -->
        <div v-if="component.featured" class="bg-gradient-to-r from-gray-400 to-gray-500 text-white px-3 py-2 rounded-bl-xl rounded-tr-3xl text-xs font-bold shadow-lg flex items-center transform hover:scale-105 transition-transform duration-200">
          <span>Featured</span>
        </div>
        <!-- NEW Badge -->
        <div v-if="component.isNew" class="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-3 py-2 rounded-bl-xl text-xs font-bold shadow-lg flex items-center transform hover:scale-105 transition-transform duration-200" :class="component.featured ? 'rounded-tr-none' : 'rounded-tr-3xl'">
          <span>NEW</span>
        </div>
      </div>

      <!-- Card Content -->
      <div class="relative p-8 space-y-6">
        
        <!-- Header Section with Icon and Title -->
        <div class="flex items-start space-x-5">
          <!-- Cool Icon Container -->
          <div class="relative">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-slate-100 to-slate-200 shadow-xl flex items-center justify-center group-hover:shadow-2xl transition-all duration-300">
              <!-- Image Icon (for file paths like .png) -->
              <img 
                v-if="component.icon.startsWith('/') || component.icon.includes('.')"
                :src="component.icon" 
                :alt="component.name" 
                class="w-10 h-10 object-contain group-hover:scale-110 transition-transform duration-300"
                @error="iconError = true"
              />
              <!-- Heroicon (for icon names like i-heroicons-*) -->
              <div 
                v-else
                :class="`text-2xl ${getIconColor(component.color)} group-hover:scale-110 transition-transform duration-300`"
              >
                <UIcon :name="component.icon" />
              </div>
              <!-- Fallback icon if image fails to load -->
              <div 
                v-if="iconError && (component.icon.startsWith('/') || component.icon.includes('.'))"
                :class="`text-2xl ${getIconColor(component.color)} group-hover:scale-110 transition-transform duration-300`"
              >
                <UIcon name="i-heroicons-cpu-chip" />
              </div>
            </div>
            <!-- Glow Effect -->
            <div class="absolute inset-0 rounded-2xl bg-gradient-to-br opacity-0 group-hover:opacity-20 transition-opacity duration-300" :class="`from-${component.color}-400 to-${component.color}-600`"></div>
          </div>
          
          <!-- Title and Category -->
          <div class="flex-1 min-w-0">
            <h3 class="text-xl font-bold text-gray-900 group-hover:text-gray-700 transition-colors duration-300 mb-2 line-clamp-2">
              {{ component.name }}
            </h3>
            <div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold transition-all duration-300"
                 :class="getCategoryStyle(component.color)">
              {{ getCategoryName(component.category) }}
            </div>
          </div>
        </div>

        <!-- Description Section -->
        <div class="bg-gray-50/50 rounded-2xl p-4">
          <p class="text-gray-600 text-sm leading-relaxed line-clamp-3">
            {{ component.description }}
          </p>
        </div>

        <!-- Tags Section -->
        <div class="flex flex-wrap gap-2">
                      <span
            v-for="tag in component.tags.slice(0, 3)"
            :key="tag"
            class="inline-flex items-center px-3 py-1 rounded-lg bg-white text-gray-600 text-xs font-medium hover:shadow-sm transition-all duration-200"
          >
            {{ tag }}
          </span>
          <span
            v-if="component.tags.length > 3"
            class="inline-flex items-center px-3 py-1 rounded-lg bg-gradient-to-r from-gray-100 to-gray-200 text-gray-500 text-xs font-medium"
          >
            +{{ component.tags.length - 3 }} more
          </span>
        </div>


      </div>

      <!-- Bottom Accent Line -->
      <div class="absolute bottom-0 left-0 right-0 h-1 opacity-60 transition-opacity duration-300 group-hover:opacity-100 rounded-b-3xl"
           :class="getBottomAccentClasses(component.color)">
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  // Adobe Tracking function - improved with multiple fallbacks
  const trackComponentClick = (component: AIComponent) => {
    try {
      // Detect environment
      const getEnvironment = () => {
        if (typeof window === 'undefined') return 'unknown'
        const hostname = window.location.hostname
        if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.includes('.local')) {
          return 'DEV'
        }
        return 'PROD'
      }

      const trackingData = {
        event: 'button_click',
        eventValue: 'Navigate to AI Assistant',
        eventInfo: {
          assistantId: component.id,
          assistantName: component.name,
          category: component.category,
          color: component.color,
          isFeatured: component.featured || false,
          isNew: component.isNew || false,
          tagCount: component.tags.length,
          clickSource: 'grid_card',
          navigationType: 'ai_assistant_click'
        },
        page: {
          title: 'ai_hub_index',
          environment: getEnvironment()
        }
      }

      if (typeof window !== 'undefined') {
        // Try Adobe DataLayer first
        if ((window as any).adobeDataLayer) {
          (window as any).adobeDataLayer.push(trackingData)
        
        }
        // Try regular dataLayer as fallback
        else if ((window as any).dataLayer) {
          (window as any).dataLayer.push(trackingData)
        
        }
        // Log tracking data even if no dataLayer available for debugging
        else {
        }
      }
    } catch (error) {
      console.error('❌ ComponentCard: Tracking error:', error)
    }
  }
  
  // Interface für AIComponent direkt hier definieren
  interface AIComponent {
    id: string
    name: string
    description: string
    category: string
    icon: string
    color: string
    component: string
    route: string
    tags: string[]
    featured?: boolean
    isNew?: boolean
  }
  
  interface Props {
    component: AIComponent
    featured?: boolean
  }
  
  const props = defineProps<Props>()
  
  // State for icon error handling
  const iconError = ref(false)
  
  const getCategoryName = (category: string) => {
    const categoryNames: Record<string, string> = {
      search: 'Search',
      creative: 'Creative',
      analysis: 'Analysis',
      development: 'Development',
      communication: 'Communication'
    }
    return categoryNames[category] || category
  }

  const getIconColor = (color: string) => {
    const colorMap: Record<string, string> = {
      blue: 'text-blue-600',
      green: 'text-green-600',
      purple: 'text-purple-600',
      orange: 'text-orange-600',
      red: 'text-red-600',
      yellow: 'text-yellow-600',
      pink: 'text-pink-600',
      indigo: 'text-indigo-600',
      cyan: 'text-cyan-600',
      teal: 'text-teal-600',
      gray: 'text-gray-600'
    }
    return colorMap[color] || 'text-gray-600'
  }

  const getCategoryStyle = (color: string) => {
    const styleMap: Record<string, string> = {
      blue: 'bg-blue-50 border-blue-200 text-blue-700',
      green: 'bg-green-50 border-green-200 text-green-700',
      purple: 'bg-purple-50 border-purple-200 text-purple-700',
      orange: 'bg-orange-50 border-orange-200 text-orange-700',
      red: 'bg-red-50 border-red-200 text-red-700',
      yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
      pink: 'bg-pink-50 border-pink-200 text-pink-700',
      indigo: 'bg-indigo-50 border-indigo-200 text-indigo-700',
      cyan: 'bg-cyan-50 border-cyan-200 text-cyan-700',
      teal: 'bg-teal-50 border-teal-200 text-teal-700',
      gray: 'bg-gray-50 border-gray-200 text-gray-700'
    }
    return styleMap[color] || 'bg-gray-50 border-gray-200 text-gray-700'
  }

  const getBottomAccentClasses = (color: string) => {
    const accentMap: Record<string, string> = {
      blue: 'bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600',
      green: 'bg-gradient-to-r from-green-400 via-green-500 to-green-600',
      purple: 'bg-gradient-to-r from-purple-400 via-purple-500 to-purple-600',
      orange: 'bg-gradient-to-r from-orange-400 via-orange-500 to-orange-600',
      red: 'bg-gradient-to-r from-red-400 via-red-500 to-red-600',
      yellow: 'bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600',
      pink: 'bg-gradient-to-r from-pink-400 via-pink-500 to-pink-600',
      indigo: 'bg-gradient-to-r from-indigo-400 via-indigo-500 to-indigo-600',
      cyan: 'bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600',
      teal: 'bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600',
      gray: 'bg-gradient-to-r from-gray-400 via-gray-500 to-gray-600'
    }
    return accentMap[color] || 'bg-gradient-to-r from-gray-400 via-gray-500 to-gray-600'
  }
  
  const navigateToComponent = async () => {
    // Track component click before navigation
    trackComponentClick(props.component)
    
    // Small delay to ensure tracking fires before navigation
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Use window.location to navigate - more reliable in components
    window.location.href = props.component.route
  }
  </script>
  
  <style scoped>
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    line-clamp: 3;
    overflow: hidden;
  }
  </style>