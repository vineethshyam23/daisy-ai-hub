import { defineStore } from 'pinia'
import { collection, doc, addDoc, updateDoc, deleteDoc, query, where, getDocs, orderBy, serverTimestamp } from 'firebase/firestore'
import { useAuthStore } from './auth'

export interface ProcessingTemplate {
  id: string
  userId: string
  assistantType: string // e.g., 'document-processor', 'multi-document-analyzer'
  title: string
  description?: string
  content: string
  createdAt: any
  updatedAt: any
}

export const useTemplateStore = defineStore('templates', () => {
  const db = useFirestore()
  const authStore = useAuthStore()
  
  // State
  const templates = ref<ProcessingTemplate[]>([])
  const isLoading = ref(false)
  const isInitialized = ref(false)
  
  // Computed
  const userTemplates = computed(() => 
    templates.value.filter(template => template.userId === authStore.user?.uid)
  )
  
  // Get templates for specific assistant
  const getTemplatesForAssistant = (assistantType: string) => 
    templates.value.filter(template => 
      template.userId === authStore.user?.uid && 
      template.assistantType === assistantType
    )
  
  // Load user's templates
  const loadUserTemplates = async () => {
    if (!authStore.user?.uid) {
      console.warn('No authenticated user, cannot load templates')
      return
    }
    
    isLoading.value = true
    
    try {
      const templatesRef = collection(db, 'processingTemplates')
      const userQuery = query(
        templatesRef,
        where('userId', '==', authStore.user.uid),
        orderBy('updatedAt', 'desc')
      )
      
      const querySnapshot = await getDocs(userQuery)
      const loadedTemplates: ProcessingTemplate[] = []
      
      querySnapshot.forEach((doc) => {
        loadedTemplates.push({
          id: doc.id,
          ...doc.data()
        } as ProcessingTemplate)
      })
      
      templates.value = loadedTemplates
      
    } catch (error) {
      console.error('Error loading user templates:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  // Create new template
  const createTemplate = async (templateData: {
    assistantType: string
    title: string
    description?: string
    content: string
  }) => {
    if (!authStore.user?.uid) {
      throw new Error('User must be authenticated to create templates')
    }
    
    isLoading.value = true
    
    try {
      const templatesRef = collection(db, 'processingTemplates')
      
      const newTemplate = {
        userId: authStore.user.uid,
        assistantType: templateData.assistantType,
        title: templateData.title.trim(),
        description: templateData.description?.trim() || '',
        content: templateData.content.trim(),
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp()
      }
      
      const docRef = await addDoc(templatesRef, newTemplate)
      
      const createdTemplate: ProcessingTemplate = {
        id: docRef.id,
        ...newTemplate,
        createdAt: new Date(),
        updatedAt: new Date()
      }
      
      templates.value.unshift(createdTemplate)
      
      return createdTemplate
      
    } catch (error) {
      console.error('Error creating template:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  // Update existing template
  const updateTemplate = async (templateId: string, updates: {
    title?: string
    description?: string
    content?: string
  }) => {
    if (!authStore.user?.uid) {
      throw new Error('User must be authenticated to update templates')
    }
    
    const template = templates.value.find(t => t.id === templateId && t.userId === authStore.user?.uid)
    if (!template) {
      throw new Error('Template not found or access denied')
    }
    
    isLoading.value = true
    
    try {
      const templateRef = doc(db, 'processingTemplates', templateId)
      
      const updateData: any = {
        updatedAt: serverTimestamp()
      }
      
      if (updates.title !== undefined) {
        updateData.title = updates.title.trim()
      }
      if (updates.description !== undefined) {
        updateData.description = updates.description.trim()
      }
      if (updates.content !== undefined) {
        updateData.content = updates.content.trim()
      }
      
      await updateDoc(templateRef, updateData)
      
      // Update local state
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index !== -1) {
        templates.value[index] = {
          ...templates.value[index],
          ...updateData,
          updatedAt: new Date()
        }
      }
      
    } catch (error) {
      console.error('Error updating template:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  // Delete template
  const deleteTemplate = async (templateId: string) => {
    if (!authStore.user?.uid) {
      throw new Error('User must be authenticated to delete templates')
    }
    
    const template = templates.value.find(t => t.id === templateId && t.userId === authStore.user?.uid)
    if (!template) {
      throw new Error('Template not found or access denied')
    }
    
    isLoading.value = true
    
    try {
      const templateRef = doc(db, 'processingTemplates', templateId)
      await deleteDoc(templateRef)
      
      // Remove from local state
      templates.value = templates.value.filter(t => t.id !== templateId)  
      
    } catch (error) {
      console.error('Error deleting template:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  // Get template by ID
  const getTemplate = (templateId: string): ProcessingTemplate | undefined => {
    return templates.value.find(t => t.id === templateId && t.userId === authStore.user?.uid)
  }
  
  // Initialize store
  const init = async () => {
    if (isInitialized.value || !authStore.user?.uid) return
    
    try {
      await loadUserTemplates()
      isInitialized.value = true
    } catch (error) {
      console.error('Error initializing template store:', error)
      // Don't throw error, allow graceful degradation
      isInitialized.value = true
    }
  }
  
  // Reset store (on logout)
  const reset = () => {
    templates.value = []
    isLoading.value = false
    isInitialized.value = false
  }
  
  return {
    // State
    templates: readonly(templates),
    isLoading: readonly(isLoading),
    isInitialized: readonly(isInitialized),
    
    // Computed
    userTemplates: readonly(userTemplates),
    
    // Methods
    getTemplatesForAssistant,
    init,
    reset,
    loadUserTemplates,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    getTemplate
  }
}) 