import {
  generateRandomApplications,
  generateRandomApplication,
} from "./Mocking";

const DB_KEY = "civitas_applications_db";

class ApplicationDatabase {
  constructor() {
    this.applications = new Map();
    this.nextId = 1;
    this.loadFromStorage();
  }

  loadFromStorage() {
    try {
      const storedData = localStorage.getItem(DB_KEY);
      if (storedData) {
        const parsedData = JSON.parse(storedData);

        if (parsedData.applications) {
          Object.entries(parsedData.applications).forEach(([id, app]) => {
            app.createdAt = new Date(app.createdAt);
            this.applications.set(parseInt(id), app);
          });
        }

        this.nextId = parsedData.nextId || this.applications.size + 1;

        console.log(
          `Loaded ${this.applications.size} applications from persistent storage`
        );
      } else {
        this.initializeWithRandomData();
      }
    } catch (error) {
      console.error("Error loading from localStorage:", error);
      this.initializeWithRandomData();
    }
  }

  saveToStorage() {
    try {
      const dataToStore = {
        applications: Object.fromEntries(this.applications),
        nextId: this.nextId,
      };
      localStorage.setItem(DB_KEY, JSON.stringify(dataToStore));
      console.log(
        `Saved ${this.applications.size} applications to persistent storage`
      );
    } catch (error) {
      console.error("Error saving to localStorage:", error);
    }
  }

  initializeWithRandomData(count = 30) {
    console.log("Initializing database with random applications...");
    const randomApps = generateRandomApplications(count);

    randomApps.forEach((app) => {
      this.applications.set(app.id, app);
    });

    this.nextId = count + 1;
    this.saveToStorage();
    console.log(`Created ${count} initial applications`);
  }

  getAllApplications() {
    return Array.from(this.applications.values());
  }

  getAllApplicationsDict() {
    return Object.fromEntries(this.applications);
  }

  getApplicationById(id) {
    return this.applications.get(id);
  }

  addApplication(applicationData = null) {
    let newApp;

    if (applicationData) {
      newApp = { ...applicationData, id: this.nextId };
    } else {
      newApp = generateRandomApplication(this.nextId);
    }

    this.applications.set(this.nextId, newApp);
    this.nextId++;
    this.saveToStorage();

    return newApp;
  }

  updateApplication(id, updates) {
    const existingApp = this.applications.get(id);
    if (existingApp) {
      const updatedApp = { ...existingApp, ...updates };
      this.applications.set(id, updatedApp);
      this.saveToStorage();
      return updatedApp;
    }
    return null;
  }

  deleteApplication(id) {
    const deleted = this.applications.delete(id);
    if (deleted) {
      this.saveToStorage();
    }
    return deleted;
  }

  getApplicationsByStatus(status) {
    return this.getAllApplications().filter((app) => app.status === status);
  }

  getApplicationsByFormId(formId) {
    return this.getAllApplications().filter((app) => app.formId === formId);
  }

  getApplicationsByApplicantId(applicantId) {
    return this.getAllApplications().filter(
      (app) => app.applicantId === applicantId
    );
  }

  searchApplications(searchTerm) {
    if (!searchTerm) return this.getAllApplications();

    const term = searchTerm.toLowerCase();
    return this.getAllApplications().filter((app) => {
      const payloadString = JSON.stringify(app.jsonPayload).toLowerCase();
      return (
        payloadString.includes(term) ||
        app.status.toLowerCase().includes(term) ||
        app.id.toString().includes(term)
      );
    });
  }

  resetDatabase() {
    this.applications.clear();
    this.nextId = 1;
    localStorage.removeItem(DB_KEY);
    this.initializeWithRandomData();
  }

  exportData() {
    return {
      applications: Object.fromEntries(this.applications),
      nextId: this.nextId,
      exportDate: new Date().toISOString(),
    };
  }

  importData(data) {
    try {
      this.applications.clear();

      if (data.applications) {
        Object.entries(data.applications).forEach(([id, app]) => {
          app.createdAt = new Date(app.createdAt);
          this.applications.set(parseInt(id), app);
        });
      }

      this.nextId = data.nextId || this.applications.size + 1;
      this.saveToStorage();

      console.log("Data imported successfully");
      return true;
    } catch (error) {
      console.error("Error importing data:", error);
      return false;
    }
  }
}

const applicationDB = new ApplicationDatabase();

export default applicationDB;

export const getAllApplications = () => applicationDB.getAllApplications();
export const getApplicationById = (id) => applicationDB.getApplicationById(id);
export const addApplication = (data) => applicationDB.addApplication(data);
export const updateApplication = (id, updates) =>
  applicationDB.updateApplication(id, updates);
export const deleteApplication = (id) => applicationDB.deleteApplication(id);
export const getApplicationsByStatus = (status) =>
  applicationDB.getApplicationsByStatus(status);
export const searchApplications = (term) =>
  applicationDB.searchApplications(term);
export const getStats = () => applicationDB.getStats();

export const useApplicationDatabase = () => {
  return {
    db: applicationDB,
    getAllApplications,
    getApplicationById,
    addApplication,
    updateApplication,
    deleteApplication,
    getApplicationsByStatus,
    searchApplications,
    getStats,
  };
};
