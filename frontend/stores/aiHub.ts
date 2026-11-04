import { defineStore } from 'pinia'
import { useRoleStore } from './roles'
import type { AIComponent } from '~/types/ai'

export const useAIHubStore = defineStore('aiHub', {
  state: () => ({
    components: [
      {
        id: 'image-generator',
        name: 'Image Generator',
        description: 'Create stunning images from text descriptions using state-of-the-art AI technology',
        category: 'creative',
        icon: 'i-heroicons-photo',
        color: 'purple',
        component: 'ImageGenerator',
        route: '/ai/image-generator',
        tags: ['images', 'creative', 'generation', 'ai'],
        featured: true,
        isNew: false
      },
      {
        id: 'email-responder',
        name: 'Email Responder',
        description: 'Generate professional and personalized email responses using AI to save time and improve communication',
        category: 'communication',
        icon: 'i-heroicons-envelope',
        color: 'indigo',
        component: 'EmailResponder',
        route: '/ai/email-responder',
        tags: ['email', 'communication', 'response', 'professional', 'writing'],
        featured: true,
        isNew: false
      },
      {
        id: 'social-media-generator',
        name: 'Social Media Post Generator',
        description: 'Create engaging social media posts and content for various platforms with AI-powered creativity',
        category: 'creative',
        icon: 'i-heroicons-hashtag',
        color: 'pink',
        component: 'SocialMediaGenerator',
        route: '/ai/social-media-generator',
        tags: ['social media', 'content', 'marketing', 'posts', 'creative'],
        featured: true,
        isNew: false
      },

      {
        id: 'meeting-summarizer',
        name: 'Meeting Summarizer',
        description: 'Transform meeting transcripts into structured summaries with key decisions, action items, and next steps',
        category: 'analysis',
        icon: 'i-heroicons-document-text',
        color: 'teal',
        component: 'MeetingSummarizer',
        route: '/ai/meeting-summarizer',
        tags: ['meetings', 'transcripts', 'summary', 'action items', 'decisions'],
        featured: true,
        isNew: false
      },
      {
        id: 'approved-metro-tools',
        name: 'Approved METRO Tools',
        description: 'Collection of approved and enterprise-ready AI services from METRO AG for secure business use',
        category: 'enterprise',
        icon: '/metro_logo.png',
        color: 'blue',
        component: 'ApprovedMetroTools',
        route: '/ai/approved-metro-tools',
        tags: ['METRO', 'Enterprise', 'Approved', 'AI Services', 'Business', 'Secure'],
        featured: true,
        isNew: false
      },

      {
        id: 'document-processor',
        name: 'Document Processor',
        description: 'Upload documents (PDF, PNG, JPG) and extract text content using OCR and AI with optional processing instructions',
        category: 'analysis',
        icon: 'i-heroicons-document-magnifying-glass',
        color: 'orange',
        component: 'DocumentProcessor',
        route: '/ai/document-processor',
        tags: ['OCR', 'document', 'text extraction', 'PDF', 'image', 'processing'],
        featured: true,
        isNew: true
      },
      {
        id: 'invoice-validator-sco',
        name: 'Invoice Validator - SCO',
        description: 'Supply-Chain Operations tool: Upload invoice and Jira Excel files to validate and compare them. Returns a downloadable Excel file with computed differences.',
        category: 'analysis',
        icon: 'i-heroicons-calculator',
        color: 'green',
        component: 'InvoiceValidatorSco',
        route: '/ai/invoice-validator-sco',
        tags: ['Excel', 'Invoice', 'Jira', 'Validation', 'SCO', 'Supply Chain', 'Comparison'],
        featured: true,
        isNew: true
      },
      {
        id: 'multi-document-analyzer',
        name: 'Multi-Document Analyzer',
        description: 'Upload multiple documents and get comprehensive AI-powered analysis with insights, comparisons, and cited references',
        category: 'analysis',
        icon: 'i-heroicons-document-duplicate',
        color: 'teal',
        component: 'MultiDocumentAnalyzer',
        route: '/ai/multi-document-analyzer',
        tags: ['analysis', 'documents', 'comparison', 'insights', 'citations', 'multi-file'],
        featured: true,
        isNew: true
      },
      {
        id: 'learning-path-creator',
        name: 'Learning Path Creator',
        description: 'Create personalized AI-generated learning paths tailored to your skill level, time commitment, and goals',
        category: 'education',
        icon: 'i-heroicons-academic-cap',
        color: 'blue',
        component: 'LearningPathCreator',
        route: '/ai/learning-path-creator',
        tags: ['learning', 'education', 'career', 'skills', 'development', 'study plan'],
        featured: true,
        isNew: true
      }
    ] as AIComponent[],
    searchQuery: '',
    viewMode: 'grid' as 'grid' | 'list',
    selectedCategory: 'all',
    customOrder: [] as string[], // Array of component IDs in custom order
    isOrderLoaded: false,
    isInitializing: false // Flag to prevent multiple simultaneous initializations
  }),

  getters: {
    // Get components in custom order if available, otherwise use default sorting
    orderedComponents: (state) => {
      if (state.customOrder.length === 0) {
        // Default sorting: Featured assistants first, then alphabetically by name
        return [...state.components].sort((a, b) => {
          if (a.featured && !b.featured) return -1
          if (!a.featured && b.featured) return 1
          return a.name.localeCompare(b.name)
        })
      }
      
      // Custom order: sort by customOrder array
      const ordered = []
      const unordered = []
      
      // First, add components in the custom order
      for (const id of state.customOrder) {
        const component = state.components.find(c => c.id === id)
        if (component) {
          ordered.push(component)
        }
      }
      
      // Then add any components not in the custom order (new components)
      for (const component of state.components) {
        if (!state.customOrder.includes(component.id)) {
          unordered.push(component)
        }
      }
      
      // Sort unordered components by name and append them
      unordered.sort((a, b) => a.name.localeCompare(b.name))
      
      return [...ordered, ...unordered]
    },

    filteredComponents: (state) => {
      let filtered = (state as any).orderedComponents

      // Filter by user role permissions
      const roleStore = useRoleStore()
      
      // Only apply role-based filtering if role store is fully initialized AND has valid permissions
      if (roleStore.isInitialized && 
          roleStore.rolePermissions && 
          roleStore.rolePermissions.allowedAssistants && 
          Array.isArray(roleStore.rolePermissions.allowedAssistants) &&
          roleStore.rolePermissions.allowedAssistants.length > 0) {
        
        try {
          filtered = filtered.filter((component: AIComponent) => 
            roleStore.hasAssistantPermission(component.id)
          )
        } catch (error) {
          console.error('Error filtering by role permissions:', error)
          // In case of error, don't filter - show all components
        }
      }

      // Filter by search term
      if (state.searchQuery) {
        const query = state.searchQuery.toLowerCase()
        filtered = filtered.filter((component: AIComponent) =>
          component.name.toLowerCase().includes(query) ||
          component.description.toLowerCase().includes(query) ||
          component.tags.some((tag: string) => tag.toLowerCase().includes(query))
        )
      }

      // Filter by category
      if (state.selectedCategory !== 'all') {
        filtered = filtered.filter((component: AIComponent) => component.category === state.selectedCategory)
      }

      return filtered
    },

    featuredComponents: (state) => {
      const roleStore = useRoleStore()
      let featured = (state as any).orderedComponents.filter((component: AIComponent) => component.featured)
      
      // Filter featured components by role permissions
      if (roleStore.isInitialized && roleStore.rolePermissions) {
        try {
          featured = featured.filter((component: AIComponent) => 
            roleStore.hasAssistantPermission(component.id)
          )
        } catch (error) {
          console.error('Error filtering featured components by role permissions:', error)
        }
      }
      
      return featured
    },

    newComponents: (state) => {
      const roleStore = useRoleStore()
      let newComps = (state as any).orderedComponents.filter((component: AIComponent) => {
        const isNew = component.isNew === true
        return isNew
      })
      
      // Filter new components by role permissions
      if (roleStore.isInitialized && roleStore.rolePermissions) {
        try {
          newComps = newComps.filter((component: AIComponent) => 
            roleStore.hasAssistantPermission(component.id)
          )
        } catch (error) {
          console.error('Error filtering new components by role permissions:', error)
        }
      }
      
      return newComps
    },

    categories: (state) => {
      const categories = [...new Set(state.components.map(c => c.category))]
      return [
        { id: 'all', name: 'All Categories' },
        ...categories.map(cat => ({
          id: cat,
          name: cat.charAt(0).toUpperCase() + cat.slice(1)
        }))
      ]
    }
  },

  actions: {
    setSearchQuery(query: string) {
      this.searchQuery = query
    },

    setViewMode(mode: 'grid' | 'list') {
      this.viewMode = mode
    },

    setSelectedCategory(category: string) {
      this.selectedCategory = category
    },

    getComponentById(id: string) {
      return this.components.find(component => component.id === id)
    },

    // Save custom order to Firebase
    async saveCustomOrder(newOrder: string[]) {
      try {
        const db = useFirestore()
        const { doc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        const orderRef = doc(db, 'settings', 'aiAssistantsOrder')
        await setDoc(orderRef, {
          order: newOrder,
          updatedAt: serverTimestamp(),
          updatedBy: 'admin' // Could be dynamic based on current user
        })
        
        this.customOrder = newOrder
        return true
      } catch (error) {
        console.error('Error saving custom order:', error)
        return false
      }
    },

    // Load custom order from Firebase
    async loadCustomOrder() {
      try {
        const db = useFirestore()
        const { doc, getDoc } = await import('firebase/firestore')
        
        const orderRef = doc(db, 'settings', 'aiAssistantsOrder')
        const orderDoc = await getDoc(orderRef)
        
        if (orderDoc.exists()) {
          const data = orderDoc.data()
          this.customOrder = data.order || []
        }
        
        // Also load featured status and NEW status
        await this.loadFeaturedStatus()
        await this.loadNewStatus()
        
        this.isOrderLoaded = true
      } catch (error) {
        console.error('Error loading custom order:', error)
        this.isOrderLoaded = true
      }
    },

    // Migration function to copy old aiTools* documents to aiAssistants* names
    async migrateOldFirestoreDocuments() {
      try {
        const db = useFirestore()
        const { doc, getDoc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        // Migration mapping: old name -> new name
        const migrations = [
          { oldName: 'aiToolsOrder', newName: 'aiAssistantsOrder' },
          { oldName: 'aiToolsFeatured', newName: 'aiAssistantsFeatured' },
          { oldName: 'aiToolsNew', newName: 'aiAssistantsNew' }
        ]
        
        for (const migration of migrations) {
          const oldRef = doc(db, 'settings', migration.oldName)
          const newRef = doc(db, 'settings', migration.newName)
          
          try {
            // Check if old document exists
            const oldDoc = await getDoc(oldRef)
            if (oldDoc.exists()) {
              // Check if new document already exists
              const newDoc = await getDoc(newRef)
              if (!newDoc.exists()) {
                // Copy data from old to new document
                const oldData = oldDoc.data()
                await setDoc(newRef, {
                  ...oldData,
                  migratedFrom: migration.oldName,
                  migratedAt: serverTimestamp()
                })
              }
            }
          } catch (migrationError) {
            console.warn(`Error migrating ${migration.oldName}:`, migrationError)
          }
        }
      } catch (error) {
        console.error('Error during migration:', error)
      }
    },

    // Load featured status from Firebase
    async loadFeaturedStatus() {
      try {
        const db = useFirestore()
        const { doc, getDoc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        const featuredRef = doc(db, 'settings', 'aiAssistantsFeatured')
        const featuredDoc = await getDoc(featuredRef)
        
        if (featuredDoc.exists()) {
          const data = featuredDoc.data()
          const featuredData = data.featured || {}
          
          // Update components with featured status from Firebase
          for (const component of this.components) {
            if (featuredData.hasOwnProperty(component.id)) {
              component.featured = featuredData[component.id]
            } else {
              // If component not in Firebase, use default value and ensure it's boolean
              component.featured = component.featured === true
            }
          }
        } else {
          try {
            // Create the initial featured status document with current default values
            const defaultFeaturedStatus: { [key: string]: boolean } = {}
            for (const component of this.components) {
              defaultFeaturedStatus[component.id] = component.featured === true
            }
            
            // Save to Firebase
            await setDoc(featuredRef, {
              featured: defaultFeaturedStatus,
              updatedAt: serverTimestamp(),
              updatedBy: 'system'
            })
          } catch (createError) {
            console.warn('Could not create featured status document (insufficient permissions):', createError)
            // Use default values without Firebase sync
          }
        }
      } catch (error) {
        console.error('Error loading featured status:', error)
      }
    },

    // Load NEW status from Firebase
    async loadNewStatus() {
      try {
        const db = useFirestore()
        const { doc, getDoc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        const newRef = doc(db, 'settings', 'aiAssistantsNew')
        const newDoc = await getDoc(newRef)
        
        if (newDoc.exists()) {
          const data = newDoc.data()
          const newData = data.isNew || {}
          
          // Update components with NEW status from Firebase
          for (const component of this.components) {
            if (newData.hasOwnProperty(component.id)) {
              component.isNew = newData[component.id]
            } else {
              // If component not in Firebase, use default value and ensure it's boolean
              component.isNew = component.isNew === true
            }
          }
        } else {
          try {
            // Create the initial NEW status document with current default values
            const defaultNewStatus: { [key: string]: boolean } = {}
            for (const component of this.components) {
              defaultNewStatus[component.id] = component.isNew === true
            }
            
            // Save to Firebase
            await setDoc(newRef, {
              isNew: defaultNewStatus,
              updatedAt: serverTimestamp(),
              updatedBy: 'system'
            })
          } catch (createError) {
            console.warn('Could not create NEW status document (insufficient permissions):', createError)
            // Use default values without Firebase sync
          }
        }
      } catch (error) {
        console.error('Error loading NEW status:', error)
      }
    },

    // Update the order of components
    updateOrder(newOrder: string[]) {
      this.customOrder = newOrder
    },

    // Initialize the store (load custom order and statuses)
    async init() {
      if (this.isInitializing) return
      
      this.isInitializing = true
      
      try {
        // First, migrate any old Firestore documents
        await this.migrateOldFirestoreDocuments()
        
        // Then load the current data
        await this.loadCustomOrder()
      } catch (error) {
        console.error('Error initializing AI Hub store:', error)
      } finally {
        this.isInitializing = false
      }
    },

    // Force reload all data from Firebase (useful for debugging)
    async forceReload() {
      this.isOrderLoaded = false
      this.isInitializing = false
      await this.init()
    },

    // Save NEW status to Firebase (for admin use)
    async saveNewStatus(newStatus: { [key: string]: boolean }) {
      try {
        const db = useFirestore()
        const { doc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        const newRef = doc(db, 'settings', 'aiAssistantsNew')
        await setDoc(newRef, {
          isNew: newStatus,
          updatedAt: serverTimestamp(),
          updatedBy: 'admin'
        })
        
        // Update local state
        for (const component of this.components) {
          if (newStatus.hasOwnProperty(component.id)) {
            component.isNew = newStatus[component.id]
          }
        }
        return true
      } catch (error) {
        console.error('Error saving NEW status:', error)
        return false
      }
    },

    // Save featured status to Firebase (for admin use)
    async saveFeaturedStatus(featuredStatus: { [key: string]: boolean }) {
      try {
        const db = useFirestore()
        const { doc, setDoc, serverTimestamp } = await import('firebase/firestore')
        
        const featuredRef = doc(db, 'settings', 'aiAssistantsFeatured')
        await setDoc(featuredRef, {
          featured: featuredStatus,
          updatedAt: serverTimestamp(),
          updatedBy: 'admin'
        })
        
        // Update local state
        for (const component of this.components) {
          if (featuredStatus.hasOwnProperty(component.id)) {
            component.featured = featuredStatus[component.id]
          }
        }
        return true
      } catch (error) {
        console.error('Error saving featured status:', error)
        return false
      }
    }
  }
})