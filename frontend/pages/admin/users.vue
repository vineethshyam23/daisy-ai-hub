<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="!authStore.isInitialized" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="w-16 h-16 bg-gray-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm animate-pulse">
          <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8 text-white" />
        </div>
        <h2 class="text-2xl font-bold text-gray-700 mb-2">
          DAISY Admin
        </h2>
        <p class="text-gray-600 font-light">Loading admin panel...</p>
      </div>
    </div>

    <!-- Access Denied -->
    <div v-else-if="!roleStore.isAdmin" class="flex items-center justify-center min-h-screen">
      <div class="text-center max-w-md mx-auto p-8">
        <div class="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <UIcon name="i-heroicons-shield-exclamation" class="w-12 h-12 text-red-500" />
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-4">Access Denied</h2>
        <p class="text-gray-600 mb-8">You need administrator privileges to access this page.</p>
        <UButton 
          @click="() => { 
            trackButtonClick('Return to Dashboard from Access Denied', { 
              userRole: roleStore.rolePermissions?.displayName || 'unknown',
              fromPage: 'admin_users'
            }); 
            $router.push('/'); 
          }" 
          color="gray" 
          size="lg"
        >
          Return to Dashboard
        </UButton>
      </div>
    </div>

    <!-- Admin Panel -->
    <div v-else>
      <AIHeader />
      
      <!-- Hero Banner -->
      <div class="relative bg-gradient-to-r from-gray-800 via-gray-600 to-gray-500 border-b border-gray-700 overflow-hidden">
        <!-- Admin Management Pattern -->
        <div class="absolute inset-0 w-1/2 right-0 top-0 opacity-8">
          <svg class="w-full h-full" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- User management icons -->
            <circle cx="320" cy="60" r="8" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <circle cx="340" cy="80" r="6" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <circle cx="360" cy="100" r="7" stroke="currentColor" stroke-width="1.5" fill="none"/>
            
            <!-- Role assignment lines -->
            <path d="M310 70 L350 90 M330 85 L365 105 M315 75 L355 95" stroke="currentColor" stroke-width="1" opacity="0.6"/>
            
            <!-- Permission grid -->
            <rect x="280" y="140" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            <rect x="295" y="140" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            <rect x="310" y="140" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            <rect x="280" y="155" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            <rect x="295" y="155" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            <rect x="310" y="155" width="12" height="12" stroke="currentColor" stroke-width="1" fill="none"/>
            
            <!-- Admin shield -->
            <path d="M350 180 L360 175 L370 180 L370 195 L360 200 L350 195 Z" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M355 185 L358 188 L365 182" stroke="currentColor" stroke-width="1.5" fill="none"/>
            
            <!-- Connection lines -->
            <path d="M325 65 L285 145 M345 85 L300 145 M365 105 L315 145" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
          </svg>
        </div>
        
        <!-- Admin Network Background -->
        <div class="absolute inset-0 w-2/3 right-0 top-0 opacity-4">
          <svg class="w-full h-full" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Network nodes for admin system -->
            <circle cx="450" cy="80" r="3" fill="currentColor"/>
            <circle cx="520" cy="120" r="2.5" fill="currentColor"/>
            <circle cx="480" cy="160" r="3.5" fill="currentColor"/>
            <circle cx="550" cy="200" r="2" fill="currentColor"/>
            <circle cx="420" cy="180" r="3" fill="currentColor"/>
            <circle cx="500" cy="240" r="2.5" fill="currentColor"/>
            <circle cx="470" cy="280" r="3" fill="currentColor"/>
            <circle cx="530" cy="320" r="2.5" fill="currentColor"/>
            
            <!-- Connecting lines -->
            <path d="M450 80 L520 120 L480 160 L550 200 M420 180 L500 240 L470 280 L530 320" 
                  stroke="currentColor" stroke-width="0.5" opacity="0.6"/>
            <path d="M450 80 L480 160 M520 120 L420 180 M480 160 L500 240" 
                  stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
          </svg>
        </div>
        
        <UContainer class="relative z-10 py-16">
          <div class="max-w-4xl">
            <div class="flex items-center mb-6">
              <div class="w-16 h-16 bg-gray-500 rounded-2xl flex items-center justify-center mr-6 border border-gray-700">
                <UIcon name="i-heroicons-users" class="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 class="text-4xl font-bold text-white mb-2">User Management</h1>
                <p class="text-xl text-gray-100">Manage user roles and permissions across the AI Hub</p>
              </div>
            </div>
          </div>
        </UContainer>
      </div>
      
      <UContainer class="py-8">

        <!-- Create New Role Form -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 mb-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">
              {{ editingRole ? 'Edit Role' : 'Create New Role' }}
            </h2>
            <button
              v-if="editingRole"
              @click="() => { 
                trackButtonClick('Cancel Role Edit', { 
                  roleId: editingRole,
                  roleName: newRole.displayName
                }); 
                cancelEdit(); 
              }"
              class="px-4 py-2 bg-orange-50 hover:bg-orange-100 border border-orange-200 hover:border-orange-300 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md flex items-center cursor-pointer"
              style="color: #ED6938; border-color: #ED6938; background-color: rgba(237, 105, 56, 0.1);"
              onmouseover="this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F';"
              onmouseout="this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938';"
            >
              <UIcon name="i-heroicons-x-mark" class="w-4 h-4 mr-1" />
              Cancel Edit
            </button>
          </div>
          
          <form @submit.prevent="createNewRole" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Display Name</label>
                <input
                  v-model="newRole.displayName"
                  type="text"
                  placeholder="e.g., Stage 4 User, Premium User"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
                  required
                  @input="generateRoleId"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Daily Token Limit</label>
                <input
                  v-model.number="newRole.dailyTokenLimit"
                  type="number"
                  min="1"
                  max="200"
                  placeholder="50"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
                  required
                />
              </div>
            </div>
            
            <!-- Auto-generated Role ID Preview -->
            <div v-if="newRole.displayName && !editingRole" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <div class="flex items-center space-x-2">
                <UIcon name="i-heroicons-information-circle" class="w-5 h-5 text-gray-600" />
                <div>
                  <p class="text-sm font-medium text-gray-800">Auto-generated Role ID</p>
                  <p class="text-sm text-gray-600">
                    <code class="bg-gray-100 px-2 py-1 rounded text-xs font-mono">{{ newRole.roleId }}</code>
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Role ID for editing (read-only) -->
            <div v-if="editingRole" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <div class="flex items-center space-x-2">
                <UIcon name="i-heroicons-lock-closed" class="w-5 h-5 text-gray-500" />
                <div>
                  <p class="text-sm font-medium text-gray-700">Role ID (cannot be changed)</p>
                  <p class="text-sm text-gray-600">
                    <code class="bg-gray-100 px-2 py-1 rounded text-xs font-mono">{{ newRole.roleId }}</code>
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                v-model="newRole.description"
                rows="2"
                placeholder="Describe this role and its purpose..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
                required
              ></textarea>
            </div>
            
            <div>
                              <label class="block text-sm font-medium text-gray-700 mb-3">Allowed Assistants</label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <div
                  v-for="(assistantName, assistantId) in availableAssistants"
                  :key="assistantId"
                  class="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <input
                    :id="`assistant-${assistantId}`"
                    v-model="newRole.allowedAssistants"
                    :value="assistantId"
                    type="checkbox"
                    class="w-4 h-4 text-gray-600 border-gray-300 rounded focus:ring-gray-500"
                  />
                  <label
                    :for="`assistant-${assistantId}`"
                    class="text-sm font-medium text-gray-700 cursor-pointer flex-1"
                  >
                    {{ assistantName }}
                  </label>
                </div>
              </div>
            </div>
            
            <div class="flex justify-end space-x-4">
              <button
                v-if="editingRole"
                @click="cancelEdit"
                type="button"
                :disabled="isCreatingRole"
                class="px-6 py-3 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                style="color: #ED6938; border: 1px solid #ED6938; background-color: rgba(237, 105, 56, 0.1);"
                onmouseover="if(!this.disabled) { this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F'; }"
                onmouseout="if(!this.disabled) { this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938'; }"
              >
                <UIcon name="i-heroicons-x-mark" class="w-4 h-4 mr-2" />
                Cancel
              </button>
              <button
                type="submit"
                :disabled="isCreatingRole"
                class="px-8 py-3 text-white rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[140px] cursor-pointer"
                style="background-color: #ED6938; border: 1px solid #ED6938;"
                onmouseover="if(!this.disabled) { this.style.backgroundColor='#D55A2F'; this.style.borderColor='#D55A2F'; }"
                onmouseout="if(!this.disabled) { this.style.backgroundColor='#ED6938'; this.style.borderColor='#ED6938'; }"
              >
                <UIcon 
                  :name="isCreatingRole ? 'i-heroicons-arrow-path' : (editingRole ? 'i-heroicons-pencil-square' : 'i-heroicons-plus')" 
                  :class="[
                    'w-4 h-4 mr-2',
                    isCreatingRole ? 'animate-spin' : ''
                  ]" 
                />
                <span v-if="isCreatingRole">{{ editingRole ? 'Updating...' : 'Creating...' }}</span>
                <span v-else>{{ editingRole ? 'Update Role' : 'Create Role' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Role Assignment Form -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 mb-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Assign Role to User</h2>
            <button
              @click="() => { 
                trackButtonClick('Refresh Users List', { 
                  currentUserCount: allUsers.length,
                  isLoading: isLoadingUsers
                }); 
                loadAllUsers(); 
              }"
              :disabled="isLoadingUsers"
              class="px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center cursor-pointer"
              style="color: #ED6938; border: 1px solid #ED6938; background-color: rgba(237, 105, 56, 0.1);"
              onmouseover="if(!this.disabled) { this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F'; }"
              onmouseout="if(!this.disabled) { this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938'; }"
            >
              <UIcon 
                :name="isLoadingUsers ? 'i-heroicons-arrow-path' : 'i-heroicons-arrow-path'" 
                :class="[
                  'w-4 h-4 mr-2',
                  isLoadingUsers ? 'animate-spin' : ''
                ]" 
              />
              {{ isLoadingUsers ? 'Loading...' : 'Refresh Users' }}
            </button>
          </div>
          
          <form @submit.prevent="assignUserRole" class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">Select User</label>
              <div class="relative">
                <select
                  v-model="newRoleAssignment.selectedUser"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 bg-white"
                  required
                >
                  <option :value="null">Select a user...</option>
                  <option
                    v-for="user in allUsers"
                    :key="user.uid"
                    :value="user"
                  >
                    {{ user.email }} ({{ user.displayName }}) - Current: {{ roleStore.allRolePermissions[user.currentRole]?.displayName || user.currentRole }}
                  </option>
                </select>
                <div v-if="isLoadingUsers" class="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <UIcon name="i-heroicons-arrow-path" class="w-4 h-4 animate-spin text-gray-400" />
                </div>
              </div>
              <p v-if="allUsers.length === 0 && !isLoadingUsers" class="text-sm text-gray-500 mt-1">
                No users found. Click "Refresh Users" to load users.
              </p>
              <p v-else-if="allUsers.length > 0" class="text-sm text-gray-500 mt-1">
                {{ allUsers.length }} user(s) found
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">New Role</label>
              <select
                v-model="newRoleAssignment.role"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 bg-white"
                required
              >
                <option value="">Select Role</option>
                <option
                  v-for="(permissions, roleName) in roleStore.allRolePermissions"
                  :key="roleName"
                  :value="roleName"
                >
                  {{ permissions.displayName }}
                </option>
              </select>
            </div>
            
            <div class="md:col-span-3 flex justify-end">
              <button
                type="submit"
                :disabled="isAssigning || !newRoleAssignment.selectedUser || !newRoleAssignment.role"
                class="px-8 py-3 text-white rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[160px] cursor-pointer"
                style="background-color: #ED6938; border: 1px solid #ED6938;"
                onmouseover="if(!this.disabled) { this.style.backgroundColor='#D55A2F'; this.style.borderColor='#D55A2F'; }"
                onmouseout="if(!this.disabled) { this.style.backgroundColor='#ED6938'; this.style.borderColor='#ED6938'; }"
              >
                <UIcon 
                  :name="isAssigning ? 'i-heroicons-arrow-path' : 'i-heroicons-user-plus'" 
                  :class="[
                    'w-4 h-4 mr-2',
                    isAssigning ? 'animate-spin' : ''
                  ]" 
                />
                {{ isAssigning ? 'Assigning...' : 'Assign Role' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Role Permissions Overview -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Role Management</h2>
          <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            <div
              v-for="(permissions, roleName) in roleStore.allRolePermissions"
              :key="roleName"
              class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-bold text-gray-900">{{ permissions.displayName }}</h3>
                <div class="flex items-center space-x-2">
                  <div class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">
                    {{ permissions.dailyTokenLimit }} tokens
                  </div>
                  <div
                    v-if="!isDefaultRole(roleName)"
                    class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium"
                  >
                    Custom
                  </div>
                </div>
              </div>
              
              <p class="text-gray-600 text-sm mb-4">{{ permissions.description }}</p>
              
              <div class="space-y-2 mb-4">
                <h4 class="font-medium text-gray-900">Allowed Assistants:</h4>
                <div class="space-y-1">
                  <div
                    v-for="assistant in permissions.allowedAssistants"
                    :key="assistant"
                    class="flex items-center space-x-2"
                  >
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-sm text-gray-700">{{ getAssistantDisplayName(assistant) }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Action buttons for all roles -->
              <div class="pt-4 border-t border-gray-100">
                <div v-if="!isDefaultRole(roleName)" class="flex space-x-3">
                  <button
                    @click="editRole(roleName, permissions)"
                    class="flex-1 flex items-center justify-center px-4 py-2.5 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer"
                    style="color: #ED6938; border: 1px solid #ED6938; background-color: rgba(237, 105, 56, 0.1);"
                    onmouseover="this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F';"
                    onmouseout="this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938';"
                  >
                    <UIcon name="i-heroicons-pencil-square" class="w-4 h-4 mr-2" />
                    Edit Role
                  </button>
                  <button
                    @click="deleteRole(roleName)"
                    :disabled="isDeletingRole === roleName"
                    class="flex-1 flex items-center justify-center px-4 py-2.5 bg-red-50 hover:bg-red-100 text-red-700 hover:text-red-800 border border-red-200 hover:border-red-300 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                  >
                    <UIcon 
                      :name="isDeletingRole === roleName ? 'i-heroicons-arrow-path' : 'i-heroicons-trash'" 
                      :class="[
                        'w-4 h-4 mr-2',
                        isDeletingRole === roleName ? 'animate-spin' : ''
                      ]" 
                    />
                    {{ isDeletingRole === roleName ? 'Deleting...' : 'Delete' }}
                  </button>
                </div>
                
                <!-- System roles have edit button only -->
                <div v-else class="flex flex-col space-y-3">
                  <button
                    @click="editRole(roleName, permissions)"
                    class="flex items-center justify-center px-4 py-2.5 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer"
                    style="color: #ED6938; border: 1px solid #ED6938; background-color: rgba(237, 105, 56, 0.1);"
                    onmouseover="this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F';"
                    onmouseout="this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938';"
                  >
                    <UIcon name="i-heroicons-pencil-square" class="w-4 h-4 mr-2" />
                    Edit Role
                  </button>
                  <div class="text-xs text-gray-500 text-center">
                    <UIcon name="i-heroicons-shield-check" class="w-3 h-3 mr-1" />
                    System Role (Edit permissions only)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Assistants Sorting Section -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-6">
            <div>
                          <h2 class="text-2xl font-bold text-gray-900">AI Assistants Sorting</h2>
            <p class="text-gray-600 mt-1">Drag and drop to reorder AI assistants on the main page</p>
            </div>
            <div class="flex items-center space-x-3">
              <button
                v-if="!isEditingOrder"
                @click="startEditingOrder"
                class="px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md cursor-pointer"
                style="color: #ED6938; border: 1px solid #ED6938; background-color: rgba(237, 105, 56, 0.1);"
                onmouseover="this.style.backgroundColor='rgba(237, 105, 56, 0.2)'; this.style.borderColor='#D55A2F';"
                onmouseout="this.style.backgroundColor='rgba(237, 105, 56, 0.1)'; this.style.borderColor='#ED6938';"
              >
                <UIcon name="i-heroicons-pencil-square" class="w-4 h-4 mr-2" />
                Edit Order
              </button>
              <div v-else class="flex items-center space-x-2">
                <button
                  @click="cancelEditingOrder"
                  :disabled="isSavingOrder"
                  class="px-4 py-2 bg-gray-50 hover:bg-gray-100 text-gray-700 hover:text-gray-800 border border-gray-200 hover:border-gray-300 rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  <UIcon name="i-heroicons-x-mark" class="w-4 h-4 mr-2" />
                  Cancel
                </button>
                <button
                  @click="saveAssistantOrder"
                  :disabled="isSavingOrder"
                  class="px-6 py-2 text-white rounded-lg font-medium transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[120px] cursor-pointer"
                  style="background-color: #ED6938; border: 1px solid #ED6938;"
                  onmouseover="if(!this.disabled) { this.style.backgroundColor='#D55A2F'; this.style.borderColor='#D55A2F'; }"
                  onmouseout="if(!this.disabled) { this.style.backgroundColor='#ED6938'; this.style.borderColor='#ED6938'; }"
                >
                  <UIcon 
                    :name="isSavingOrder ? 'i-heroicons-arrow-path' : 'i-heroicons-check'" 
                    :class="[
                      'w-4 h-4 mr-2',
                      isSavingOrder ? 'animate-spin' : ''
                    ]" 
                  />
                  {{ isSavingOrder ? 'Saving...' : 'Save Order' }}
                </button>
              </div>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <div v-if="!isEditingOrder" class="space-y-3">
              <div
                v-for="(component, index) in aiHub.orderedComponents"
                :key="component.id"
                class="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div class="flex-shrink-0 w-8 h-8 bg-gray-200 rounded-lg flex items-center justify-center">
                  <span class="text-sm font-medium text-gray-600">{{ index + 1 }}</span>
                </div>
                <div class="flex-shrink-0">
                  <div v-if="component.icon.startsWith('/')" class="w-10 h-10 rounded-lg overflow-hidden bg-gray-100 flex items-center justify-center">
                    <img 
                      :src="component.icon" 
                      :alt="component.name"
                      class="w-6 h-6 object-contain"
                      @error="() => {}"
                    />
                  </div>
                  <div v-else :class="[
                    'w-10 h-10 rounded-lg flex items-center justify-center',
                    getIconBgColor(component.color)
                  ]">
                    <UIcon :name="component.icon" class="w-6 h-6 text-white" />
                  </div>
                </div>
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{{ component.name }}</h3>
                  <p class="text-sm text-gray-500">{{ getCategoryName(component.category) }}</p>
                </div>
                <div class="flex-shrink-0 flex items-center space-x-4">
                  <!-- Featured Status Display -->
                  <div class="flex items-center space-x-1">
                    <UIcon 
                      name="i-heroicons-star" 
                      :class="[
                        'w-4 h-4',
                        component.featured ? 'text-yellow-500' : 'text-gray-300'
                      ]" 
                    />
                    <span 
                      class="text-sm font-medium"
                      :class="component.featured ? 'text-gray-900' : 'text-gray-500'"
                    >
                      {{ component.featured ? 'Featured' : 'Standard' }}
                    </span>
                  </div>
                  <!-- NEW Status Display -->
                  <div class="flex items-center space-x-1">
                    <UIcon 
                      name="i-heroicons-sparkles" 
                      :class="[
                        'w-4 h-4',
                        component.isNew ? 'text-orange-500' : 'text-gray-300'
                      ]" 
                    />
                    <span 
                      class="text-sm font-medium"
                      :class="component.isNew ? 'text-gray-900' : 'text-gray-500'"
                    >
                      {{ component.isNew ? 'NEW' : 'Standard' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Draggable List -->
            <div v-else>
              <p class="text-sm text-gray-600 mb-4">
                <UIcon name="i-heroicons-information-circle" class="w-4 h-4 mr-1" />
                Drag and drop the assistants below to reorder them. Use the checkboxes to toggle featured and NEW status. The order will be reflected on the main page.
              </p>
              <draggable
                v-model="editableOrder"
                item-key="id"
                handle=".drag-handle"
                :animation="200"
                ghost-class="ghost"
                class="space-y-3"
              >
                <template #item="{ element: component, index }">
                  <div class="flex items-center space-x-4 p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-gray-300 transition-colors cursor-move">
                    <div class="drag-handle flex-shrink-0 w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center justify-center cursor-grab active:cursor-grabbing transition-colors">
                      <UIcon name="i-heroicons-bars-3" class="w-5 h-5 text-gray-500" />
                    </div>
                    <div class="flex-shrink-0 w-8 h-8 bg-gray-200 rounded-lg flex items-center justify-center">
                      <span class="text-sm font-medium text-gray-600">{{ index + 1 }}</span>
                    </div>
                    <div class="flex-shrink-0">
                      <div v-if="component.icon.startsWith('/')" class="w-10 h-10 rounded-lg overflow-hidden bg-gray-100 flex items-center justify-center">
                        <img 
                          :src="component.icon" 
                          :alt="component.name"
                          class="w-6 h-6 object-contain"
                          @error="() => {}"
                        />
                      </div>
                      <div v-else :class="[
                        'w-10 h-10 rounded-lg flex items-center justify-center',
                        getIconBgColor(component.color)
                      ]">
                        <UIcon :name="component.icon" class="w-6 h-6 text-white" />
                      </div>
                    </div>
                    <div class="flex-1">
                      <h3 class="font-medium text-gray-900">{{ component.name }}</h3>
                      <p class="text-sm text-gray-500">{{ getCategoryName(component.category) }}</p>
                    </div>
                    <div class="flex-shrink-0 flex items-center space-x-4">
                      <!-- Featured Toggle -->
                      <div class="flex items-center space-x-2">
                        <input
                          :id="`featured-${component.id}`"
                          v-model="component.featured"
                          @change="toggleFeaturedStatus(component)"
                          type="checkbox"
                          class="w-4 h-4 text-yellow-500 bg-white border-gray-300 rounded focus:ring-yellow-400 focus:ring-2 cursor-pointer"
                        />
                        <label
                          :for="`featured-${component.id}`"
                          class="text-sm font-medium cursor-pointer"
                          :class="component.featured ? 'text-gray-900' : 'text-gray-600'"
                        >
                          Featured
                        </label>
                        <UIcon 
                          name="i-heroicons-star" 
                          :class="[
                            'w-4 h-4',
                            component.featured ? 'text-yellow-500' : 'text-gray-300'
                          ]" 
                        />
                      </div>
                      
                      <!-- NEW Toggle -->
                      <div class="flex items-center space-x-2">
                        <input
                          :id="`new-${component.id}`"
                          v-model="component.isNew"
                          @change="toggleNewStatus(component)"
                          type="checkbox"
                          class="w-4 h-4 text-orange-500 bg-white border-gray-300 rounded focus:ring-orange-400 focus:ring-2 cursor-pointer"
                        />
                        <label
                          :for="`new-${component.id}`"
                          class="text-sm font-medium cursor-pointer"
                          :class="component.isNew ? 'text-gray-900' : 'text-gray-600'"
                        >
                          NEW
                        </label>
                        <UIcon 
                          name="i-heroicons-sparkles" 
                          :class="[
                            'w-4 h-4',
                            component.isNew ? 'text-orange-500' : 'text-gray-300'
                          ]" 
                        />
                      </div>
                    </div>
                  </div>
                </template>
              </draggable>
            </div>
          </div>
        </div>
      </UContainer>
    </div>
    
    <!-- Global Footer -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useRoleStore } from '~/stores/roles'
import { useAIHubStore } from '~/stores/aiHub'
import { useAdobeTracking } from '~/composables/useAdobeTracking'
import draggable from 'vuedraggable'

// Stores
const authStore = useAuthStore()
const roleStore = useRoleStore()
const aiHub = useAIHubStore()

// Adobe Tracking
const { trackButtonClick, trackError } = useAdobeTracking()

// State
const isAssigning = ref(false)
const isCreatingRole = ref(false)
const isDeletingRole = ref('')
const editingRole = ref(null)
const isLoadingUsers = ref(false)
const allUsers = ref([])

        // AI Assistants Sorting State
const isEditingOrder = ref(false)
const isSavingOrder = ref(false)
const editableOrder = ref([])
const featuredChanges = ref(new Map()) // Track featured status changes
const newChanges = ref(new Map()) // Track NEW status changes

const newRoleAssignment = ref({
  selectedUser: null,
  role: ''
})
const newRole = ref({
  roleId: '',
  displayName: '',
  description: '',
  dailyTokenLimit: 50,
  allowedAssistants: []
})

// Watch for displayName changes to auto-generate roleId
watch(() => newRole.value.displayName, () => {
  if (!editingRole.value) {
    generateRoleId()
  }
})

// Assistant display names mapping
const assistantDisplayNames = {
  'email-responder': 'Email Responder',
  'social-media-generator': 'Social Media Generator',
  'image-generator': 'Image Generator',
  'meeting-summarizer': 'Meeting Summarizer',
  'approved-metro-tools': 'Approved External Tools',
  'document-processor': 'Document Processor',
  'invoice-validator-sco': 'Invoice Validator - SCO',
  'multi-document-analyzer': 'Multi-Document Analyzer',
  'learning-path-creator': 'Learning Path Creator'
}

// Available assistants for role creation
const availableAssistants = {
  'email-responder': 'Email Responder',
  'social-media-generator': 'Social Media Generator',
  'image-generator': 'Image Generator',
  'meeting-summarizer': 'Meeting Summarizer',
  'approved-metro-tools': 'Approved External Tools',
  'document-processor': 'Document Processor',
  'invoice-validator-sco': 'Invoice Validator - SCO',
  'multi-document-analyzer': 'Multi-Document Analyzer',
  'learning-path-creator': 'Learning Path Creator'
}

// Methods
const getAssistantDisplayName = (assistantId) => {
  return assistantDisplayNames[assistantId] || assistantId
}

const isDefaultRole = (roleName) => {
  return ['admin', 'standard'].includes(roleName)
}

const editRole = (roleName, permissions) => {
  // Track edit role action
  trackButtonClick('Edit Role', {
    roleId: roleName,
    displayName: permissions.displayName,
    dailyTokenLimit: permissions.dailyTokenLimit,
    allowedAssistantsCount: permissions.allowedAssistants.length,
    isDefaultRole: isDefaultRole(roleName)
  })
  
  // Set the form to edit mode
  newRole.value = {
    roleId: roleName,
    displayName: permissions.displayName,
    description: permissions.description,
    dailyTokenLimit: permissions.dailyTokenLimit,
    allowedAssistants: [...permissions.allowedAssistants]
  }
  editingRole.value = roleName
  
  // Scroll to form
  const formElement = document.querySelector('form')
  if (formElement) {
    formElement.scrollIntoView({ behavior: 'smooth' })
  }
}

const deleteRole = async (roleName) => {
  if (!confirm(`Are you sure you want to delete the role "${roleName}"? This action cannot be undone.`)) {
    return
  }

  // Track role deletion attempt
  trackButtonClick('Delete Role', {
    roleId: roleName,
    displayName: roleStore.allRolePermissions[roleName]?.displayName || 'unknown',
    isDefaultRole: isDefaultRole(roleName)
  })

  isDeletingRole.value = roleName
  
  try {
    const db = useFirestore()
    const { doc, deleteDoc } = await import('firebase/firestore')
    
    const roleRef = doc(db, 'rolePermissions', roleName)
    await deleteDoc(roleRef)
    
    // Reload role store
    await roleStore.loadAllRolePermissions()
    
    // Show success toast
    const toast = useToast()
    toast.add({
      title: 'Role Deleted',
      description: `Successfully deleted role "${roleName}"`,
      color: 'green'
    })
    
  } catch (error) {
    console.error('Error deleting role:', error)
    
    // Track role deletion error
    trackError('admin_role_deletion_failed', `Failed to delete role: ${roleName}`, {
      roleId: roleName,
      displayName: roleStore.allRolePermissions[roleName]?.displayName || 'unknown',
      isDefaultRole: isDefaultRole(roleName),
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Deletion Failed',
      description: 'Failed to delete role. Please try again.',
      color: 'red'
    })
  } finally {
    isDeletingRole.value = ''
  }
}

const generateRoleId = () => {
  if (!newRole.value.displayName || editingRole.value) return
  
  // Convert display name to role ID
  let roleId = newRole.value.displayName
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '') // Remove special characters
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .replace(/^-+|-+$/g, '') // Remove leading/trailing hyphens
    .substring(0, 30) // Limit length
  
  // Ensure uniqueness by checking existing roles
  let counter = 1
  let originalRoleId = roleId
  
  while (roleStore.allRolePermissions[roleId]) {
    roleId = `${originalRoleId}-${counter}`
    counter++
  }
  
  newRole.value.roleId = roleId
}

const cancelEdit = () => {
  editingRole.value = null
  newRole.value = {
    roleId: '',
    displayName: '',
    description: '',
    dailyTokenLimit: 50,
    allowedAssistants: []
  }
}

const loadAllUsers = async () => {
  isLoadingUsers.value = true
  
  try {
    // Get all users from Firebase Auth via Admin SDK
    // Since we can't directly access Firebase Auth users from client-side,
    // we'll get users from userRoles collection and combine with any additional logic
    const db = useFirestore()
    const { collection, getDocs } = await import('firebase/firestore')
    
    // Get all user roles to find existing users
    const userRolesRef = collection(db, 'userRoles')
    const userRolesSnapshot = await getDocs(userRolesRef)
    
    const users = []
    userRolesSnapshot.forEach(doc => {
      const userData = doc.data()
      users.push({
        uid: doc.id,
        email: userData.email,
        displayName: userData.displayName || userData.email.split('@')[0],
        currentRole: userData.role,
        isActive: userData.isActive
      })
    })
    
    // Sort users by email
    users.sort((a, b) => a.email.localeCompare(b.email))
    
    allUsers.value = users
    
  } catch (error) {
    console.error('Error loading users:', error)
    
    // Track user loading error
    trackError('admin_user_loading_failed', 'Failed to load users from Firestore', {
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown',
      collection: 'userRoles',
      operation: 'getDocs'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Loading Failed',
      description: 'Failed to load users. Please try again.',
      color: 'red'
    })
  } finally {
    isLoadingUsers.value = false
  }
}

const createNewRole = async () => {
  // Generate role ID if creating new role
  if (!editingRole.value) {
    generateRoleId()
  }
  
  if (!newRole.value.roleId || !newRole.value.displayName || !newRole.value.description || newRole.value.allowedAssistants.length === 0) {
    const toast = useToast()
    toast.add({
      title: 'Validation Error',
      description: 'Please fill in all fields and select at least one assistant.',
      color: 'red'
    })
    return
  }

  // Track role creation/update attempt
  trackButtonClick(editingRole.value ? 'Update Role Submit' : 'Create Role Submit', {
    roleId: newRole.value.roleId,
    displayName: newRole.value.displayName,
    dailyTokenLimit: newRole.value.dailyTokenLimit,
    allowedAssistantsCount: newRole.value.allowedAssistants.length,
    isEdit: !!editingRole.value
  })

  // Check if role ID already exists when creating (not editing)
  if (!editingRole.value && roleStore.allRolePermissions[newRole.value.roleId]) {
    const toast = useToast()
    toast.add({
      title: 'Role Already Exists',
      description: 'A role with this ID already exists. Please try a different display name.',
      color: 'red'
    })
    return
  }

  isCreatingRole.value = true
  
  try {
    const db = useFirestore()
    const { doc, setDoc, updateDoc, serverTimestamp } = await import('firebase/firestore')
    
    const rolePermissions = {
      roleName: newRole.value.roleId,
      displayName: newRole.value.displayName,
      description: newRole.value.description,
      dailyTokenLimit: newRole.value.dailyTokenLimit,
      allowedAssistants: newRole.value.allowedAssistants,
      updatedAt: serverTimestamp(),
      updatedBy: authStore.user?.uid || 'unknown'
    }

    const roleRef = doc(db, 'rolePermissions', newRole.value.roleId)
    
    if (editingRole.value) {
      // Update existing role
      await updateDoc(roleRef, rolePermissions)
    } else {
      // Create new role
      rolePermissions.createdAt = serverTimestamp()
      rolePermissions.createdBy = authStore.user?.uid || 'unknown'
      await setDoc(roleRef, rolePermissions)
    }
    
    // Reload role store
    await roleStore.loadAllRolePermissions()
    
    // Show success toast
    const toast = useToast()
    toast.add({
      title: editingRole.value ? 'Role Updated!' : 'Role Created!',
      description: `Successfully ${editingRole.value ? 'updated' : 'created'} role "${rolePermissions.displayName}"`,
      color: 'green'
    })
    
    // Reset form
    cancelEdit()
    
  } catch (error) {
    console.error('Error saving role:', error)
    
    // Track role creation/update error
    trackError('admin_role_save_failed', `Failed to ${editingRole.value ? 'update' : 'create'} role: ${newRole.value.displayName}`, {
      roleId: newRole.value.roleId,
      displayName: newRole.value.displayName,
      dailyTokenLimit: newRole.value.dailyTokenLimit,
      allowedAssistantsCount: newRole.value.allowedAssistants.length,
      isEdit: !!editingRole.value,
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown',
      operation: editingRole.value ? 'update' : 'create'
    })
    
    const toast = useToast()
    toast.add({
      title: editingRole.value ? 'Update Failed' : 'Creation Failed',
      description: 'Failed to save role. Please try again.',
      color: 'red'
    })
  } finally {
    isCreatingRole.value = false
  }
}

const assignUserRole = async () => {
  if (!newRoleAssignment.value.selectedUser || !newRoleAssignment.value.role) {
    const toast = useToast()
    toast.add({
      title: 'Validation Error',
      description: 'Please select a user and role.',
      color: 'red'
    })
    return
  }

  // Track role assignment attempt
  trackButtonClick('Assign User Role', {
    newRole: newRoleAssignment.value.role,
    previousRole: newRoleAssignment.value.selectedUser.currentRole,
    userEmail: newRoleAssignment.value.selectedUser.email.split('@')[1] || 'unknown',
    totalUsersLoaded: allUsers.value.length
  })

  isAssigning.value = true
  
  try {
    const success = await roleStore.assignRole(
      newRoleAssignment.value.selectedUser.uid,
      newRoleAssignment.value.selectedUser.email,
      newRoleAssignment.value.role
    )
    
    if (success) {
      // Reload users to get updated roles
      await loadAllUsers()
      
      // Reset form
      const assignedUserEmail = newRoleAssignment.value.selectedUser.email
      const assignedRole = newRoleAssignment.value.role
      
      newRoleAssignment.value = {
        selectedUser: null,
        role: ''
      }
      
      // Show success toast
      const toast = useToast()
      toast.add({
        title: 'Role Assigned',
        description: `Successfully assigned ${assignedRole} role to ${assignedUserEmail}`,
        color: 'green'
      })
    }
  } catch (error) {
    console.error('Error assigning role:', error)
    
    // Track role assignment error
    trackError('admin_role_assignment_failed', `Failed to assign role to user: ${newRoleAssignment.value.selectedUser.email}`, {
      newRole: newRoleAssignment.value.role,
      previousRole: newRoleAssignment.value.selectedUser.currentRole,
      userEmail: newRoleAssignment.value.selectedUser.email.split('@')[1] || 'unknown',
      userId: newRoleAssignment.value.selectedUser.uid,
      totalUsersLoaded: allUsers.value.length,
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Assignment Failed',
      description: 'Failed to assign role. Please try again.',
      color: 'red'
    })
  } finally {
    isAssigning.value = false
  }
}

// AI Assistants Sorting Methods
const startEditingOrder = () => {
  // Track edit order action
  trackButtonClick('Start Edit AI Assistants Order', {
    totalComponents: aiHub.orderedComponents.length,
    featuredCount: aiHub.orderedComponents.filter(c => c.featured).length,
    newCount: aiHub.orderedComponents.filter(c => c.isNew).length
  })
  
  isEditingOrder.value = true
  // Create a deep copy to avoid mutating the original components
  editableOrder.value = aiHub.orderedComponents.map(component => ({
    ...component,
    featured: component.featured, // Ensure featured status is copied
    isNew: component.isNew // Ensure NEW status is copied
  }))
  featuredChanges.value.clear() // Reset changes tracker
  newChanges.value.clear() // Reset NEW changes tracker
}

const cancelEditingOrder = () => {
  // Track cancel edit order action
  trackButtonClick('Cancel AI Assistants Order Edit', {
    totalChanges: featuredChanges.value.size + newChanges.value.size,
    featuredChanges: featuredChanges.value.size,
    newChanges: newChanges.value.size
  })
  
  isEditingOrder.value = false
  editableOrder.value = []
  featuredChanges.value.clear() // Reset changes tracker
  newChanges.value.clear() // Reset NEW changes tracker
}

const toggleFeaturedStatus = (component) => {
  // Track featured toggle action
  trackButtonClick('Toggle Component Featured Status', {
    componentId: component.id,
    componentName: component.name,
    newFeaturedStatus: component.featured,
    category: component.category
  })
  
  // Track the change for saving later
  featuredChanges.value.set(component.id, component.featured)
}

const toggleNewStatus = (component) => {
  // Track NEW toggle action
  trackButtonClick('Toggle Component NEW Status', {
    componentId: component.id,
    componentName: component.name,
    newNewStatus: component.isNew,
    category: component.category
  })
  
  // Track the change for saving later
  newChanges.value.set(component.id, component.isNew)
}

const saveAssistantOrder = async () => {
  // Track save order action
  trackButtonClick('Save AI Assistants Order', {
    totalComponents: editableOrder.value.length,
    orderChanges: true, // Always true since we're saving
    featuredChanges: featuredChanges.value.size,
    newChanges: newChanges.value.size,
    totalChanges: featuredChanges.value.size + newChanges.value.size
  })
  
  isSavingOrder.value = true
  
  try {
    // Save the order
    const newOrder = editableOrder.value.map(component => component.id)
    const orderSuccess = await aiHub.saveCustomOrder(newOrder)
    
    if (!orderSuccess) {
      throw new Error('Failed to save order')
    }

    // Save featured status changes if any
    if (featuredChanges.value.size > 0) {
      const featuredSuccess = await saveFeaturedChanges()
      if (!featuredSuccess) {
        throw new Error('Failed to save featured status changes')
      }
    }

    // Save NEW status changes if any
    if (newChanges.value.size > 0) {
      const newSuccess = await saveNewChanges()
      if (!newSuccess) {
        throw new Error('Failed to save NEW status changes')
      }
    }
    
    // The store methods already update the local state, so no manual update needed
    
    isEditingOrder.value = false
    editableOrder.value = []
    featuredChanges.value.clear()
    newChanges.value.clear()
    
    const toast = useToast()
    toast.add({
      title: 'Changes Saved',
      description: 'AI assistants order, featured status, and NEW status have been updated successfully',
      color: 'green'
    })
  } catch (error) {
    console.error('Error saving assistant changes:', error)
    
    // Track AI assistants order save error
    trackError('admin_assistants_order_save_failed', 'Failed to save AI assistants order and status changes', {
      totalComponents: editableOrder.value.length,
      featuredChanges: featuredChanges.value.size,
      newChanges: newChanges.value.size,
      totalChanges: featuredChanges.value.size + newChanges.value.size,
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown',
      operation: 'save_assistants_order'
    })
    
    const toast = useToast()
    toast.add({
      title: 'Save Failed',
      description: 'Failed to save AI assistants changes. Please try again.',
      color: 'red'
    })
  } finally {
    isSavingOrder.value = false
  }
}

const saveFeaturedChanges = async () => {
  try {
    // Build complete featured status object (not just changes)
    const allFeaturedStatus = {}
    for (const component of aiHub.components) {
      // Use the change if it exists, otherwise use current status
      allFeaturedStatus[component.id] = featuredChanges.value.has(component.id) 
        ? featuredChanges.value.get(component.id)
        : component.featured
    }
    
    // Use the AI Hub store method to ensure proper synchronization
    const success = await aiHub.saveFeaturedStatus(allFeaturedStatus)
    return success
  } catch (error) {
    console.error('Error saving featured changes:', error)
    return false
  }
}

const saveNewChanges = async () => {
  try {
    // Build complete NEW status object (not just changes)
    const allNewStatus = {}
    for (const component of aiHub.components) {
      // Use the change if it exists, otherwise use current status
      allNewStatus[component.id] = newChanges.value.has(component.id) 
        ? newChanges.value.get(component.id)
        : component.isNew
    }
    
    // Use the AI Hub store method to ensure proper synchronization
    const success = await aiHub.saveNewStatus(allNewStatus)
    return success
  } catch (error) {
    console.error('Error saving NEW changes:', error)
    return false
  }
}

// Helper methods for component styling
const getIconBgColor = (color) => {
  const colorMap = {
    purple: 'bg-purple-500',
    indigo: 'bg-indigo-500',
    pink: 'bg-pink-500',
    blue: 'bg-blue-500',
    cyan: 'bg-cyan-500',
    teal: 'bg-teal-500',
    orange: 'bg-orange-500',
    green: 'bg-green-500'
  }
  return colorMap[color] || 'bg-gray-500'
}

const getCategoryName = (category) => {
  const categoryNames = {
    search: 'Search',
    creative: 'Creative',
    analysis: 'Analysis',
    development: 'Development',
    communication: 'Communication',
    education: 'Education',
    enterprise: 'Enterprise'
  }
  return categoryNames[category] || category
}

// Auth check and initialization
onMounted(async () => {
  // Wait for auth store to be initialized
  if (!authStore.isInitialized) {
    await authStore.init()
  }
  
  // Redirect to login if not authenticated
  if (!authStore.isAuthenticated) {
    await navigateTo('/login')
    return
  }

  // Initialize role store
  if (!roleStore.isInitialized) {
    await roleStore.init()
  }
  
  // Redirect if not admin
  if (!roleStore.isAdmin) {
    await navigateTo('/')
    return
  }

  // Initialize AI Hub store and wait for completion
  try {
    await aiHub.init()
    
    // Log current status for debugging
    aiHub.components.forEach(component => {

    })
  } catch (error) {
    console.error('Admin: Error initializing AI Hub store:', error)
    
    // Track AI Hub store initialization error in admin page
    trackError('admin_aihub_init_failed', 'Failed to initialize AI Hub store in admin panel', {
      errorMessage: error.message || error.toString(),
      errorCode: error.code || 'unknown',
      adminUserId: authStore.user?.uid || 'unknown',
      isAuthenticated: authStore.isAuthenticated,
      hasUser: !!authStore.user,
      isAdmin: roleStore.isAdmin,
      page: 'admin_users'
    })
  }
  
  // Load all users for role assignment
  await loadAllUsers()
})

// SEO
useHead({
  title: 'User Management - DAISY Admin',
  meta: [
    {
      name: 'description',
      content: 'Admin panel for managing user roles and permissions in DAISY.'
    }
  ]
})
</script>

<style scoped>
.ghost {
  opacity: 0.5;
  background: #f3f4f6;
  border: 2px dashed #d1d5db;
}

.drag-handle:hover {
  background-color: #f3f4f6;
}

.drag-handle:active {
  background-color: #e5e7eb;
}
</style> 