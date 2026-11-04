import { getFirestore, connectFirestoreEmulator, initializeFirestore, enableNetwork, disableNetwork, type Firestore } from 'firebase/firestore'
import { getApps } from 'firebase/app'

// Create a singleton Firestore instance to prevent multiple connections
let firestoreInstance: Firestore | null = null

export const useFirestore = () => {
  // Return existing instance if available
  if (firestoreInstance) {
    return firestoreInstance
  }
  
  // Ensure Firebase app is already initialized (by auth plugin)
  const apps = getApps()
  
  if (apps.length === 0) {
    throw new Error('Firebase app not initialized. Auth plugin should run first.')
  }

  try {
    // Check if Firestore is already initialized for this app
    try {
      firestoreInstance = getFirestore(apps[0])
    } catch (error) {
      // If not initialized, initialize with optimized settings to reduce connection errors
      firestoreInstance = initializeFirestore(apps[0], {
        cacheSizeBytes: 1048576, // 1MB cache
        experimentalForceLongPolling: true, // Use long polling instead of WebSocket to reduce connection errors
        ignoreUndefinedProperties: true,
        // Disable offline persistence to reduce connection complexity
      })
    }
    
    return firestoreInstance
  } catch (error) {
    throw error
  }
} 