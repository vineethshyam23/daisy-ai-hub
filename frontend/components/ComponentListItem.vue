<template>
  <div 
    class="group cursor-pointer transition-all duration-500 hover:scale-[1.01] hover:-translate-y-1"
    @click="navigateToComponent"
  >
    <!-- Modern List Card -->
    <div class="relative bg-white rounded-2xl shadow-lg hover:shadow-2xl backdrop-blur-xl overflow-hidden transition-all duration-500">
      
      <!-- Gradient Background Overlay -->
      <div class="absolute inset-0 bg-gradient-to-r from-orange-50/20 via-transparent to-purple-50/10 pointer-events-none"></div>
      
      <!-- Badges Container -->
      <div class="absolute top-0 right-0 z-10 flex flex-col space-y-1">
        <!-- Featured Badge -->
        <div v-if="component.featured" class="bg-gradient-to-r from-gray-400 to-gray-500 text-white px-3 py-1.5 rounded-bl-lg rounded-tr-2xl text-xs font-bold shadow-md flex items-center">
          <span>Featured</span>
        </div>
        <!-- NEW Badge -->
        <div v-if="component.isNew" class="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-3 py-1.5 rounded-bl-lg text-xs font-bold shadow-md flex items-center" :class="component.featured ? 'rounded-tr-none' : 'rounded-tr-2xl'">
          <span>NEW</span>
        </div>
      </div>
      
      <!-- Card Content -->
      <div class="relative p-6">
        <div class="flex items-center justify-between">
          
          <!-- Left Section with Icon and Content -->
          <div class="flex items-center space-x-6 flex-1 min-w-0">
            
            <!-- Cool Icon Container -->
            <div class="relative flex-shrink-0">
              <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 shadow-lg flex items-center justify-center group-hover:shadow-xl transition-all duration-300">
                <!-- Image Icon (for file paths like .png) -->
                <img 
                  v-if="component.icon.startsWith('/') || component.icon.includes('.')"
                  :src="component.icon" 
                  :alt="component.name" 
                  class="w-8 h-8 object-contain group-hover:scale-110 transition-transform duration-300"
                />
                <!-- Heroicon (for icon names like i-heroicons-*) -->
                <div 
                  v-else
                  :class="`text-xl ${getIconColor(component.color)} group-hover:scale-110 transition-transform duration-300`"
                >
                  <UIcon :name="component.icon" />
                </div>
              </div>
              <!-- Glow Effect -->
              <div class="absolute inset-0 rounded-xl bg-gradient-to-br opacity-0 group-hover:opacity-15 transition-opacity duration-300" :class="`from-${component.color}-400 to-${component.color}-600`"></div>
            </div>
            
            <!-- Content Section -->
            <div class="flex-1 min-w-0">
              
              <!-- Title and Category Row -->
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-lg font-bold text-gray-900 group-hover:text-gray-700 transition-colors duration-300 truncate">
                  {{ component.name }}
                </h3>
                <div class="inline-flex items-center px-2 py-1 rounded-lg text-xs font-semibold transition-all duration-300"
                     :class="getCategoryStyle(component.color)">
                  {{ getCategoryName(component.category) }}
                </div>
              </div>
              
              <!-- Description -->
              <p class="text-gray-600 text-sm leading-relaxed mb-3 line-clamp-2">
                {{ component.description }}
              </p>
              
              <!-- Tags Row -->
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in component.tags.slice(0, 4)"
                  :key="tag"
                  class="inline-flex items-center px-2 py-1 rounded-md bg-gray-100 text-gray-600 text-xs font-medium hover:shadow-sm transition-all duration-200"
                >
                  {{ tag }}
                </span>
                <span
                  v-if="component.tags.length > 4"
                  class="inline-flex items-center px-2 py-1 rounded-md bg-gradient-to-r from-gray-100 to-gray-200 text-gray-500 text-xs font-medium"
                >
                  +{{ component.tags.length - 4 }}
                </span>
              </div>
            </div>
          </div>


        </div>
      </div>

      <!-- Bottom Accent Line -->
      <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r opacity-50 transition-opacity duration-300 group-hover:opacity-80"
           :class="`from-${component.color}-400 via-${component.color}-500 to-${component.color}-600`">
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
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
          clickSource: 'list_item',
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
      console.error('❌ ComponentListItem: Tracking error:', error)
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
  }
  
  const props = defineProps<Props>()
  
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
  
  const navigateToComponent = async () => {
    // Track component click before navigation
    trackComponentClick(props.component)
    
    // Small delay to ensure tracking fires before navigation
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Use window.location to navigate - more reliable in components
    window.location.href = props.component.route
  }
  </script>