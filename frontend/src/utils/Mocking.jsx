import { ApplicationStatus } from "./const";

const randomInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

const randomDate = () => {
  const now = new Date();
  const oneYearAgo = new Date(
    now.getFullYear() - 1,
    now.getMonth(),
    now.getDate()
  );
  const randomTime =
    oneYearAgo.getTime() +
    Math.random() * (now.getTime() - oneYearAgo.getTime());
  return new Date(randomTime);
};

const generateRandomJsonPayload = (formId) => {
  const formTypes = {
    1: {
      // Dog
      formType: "Dog License",
      dogName: ["Buddy", "Max", "Charlie", "Lucy", "Bailey", "Cooper", "Bella"][
        randomInt(0, 6)
      ],
      dogBreed: [
        "Labrador",
        "Golden Retriever",
        "German Shepherd",
        "Bulldog",
        "Poodle",
        "Beagle",
      ][randomInt(0, 5)],
      dogAge: randomInt(1, 15),
      ownerName: [
        "John Smith",
        "Jane Doe",
        "Mike Johnson",
        "Sarah Wilson",
        "David Brown",
      ][randomInt(0, 4)],
      ownerAddress: `${randomInt(100, 9999)} Main St, City, State ${randomInt(
        10000,
        99999
      )}`,
      vaccinationRecord: Math.random() > 0.5,
    },
    2: {
      // Biike Fire
      formType: "Fire Permit",
      permitType: ["Bonfire", "Fireworks", "Burn Pile", "Special Event"][
        randomInt(0, 3)
      ],
      location: `${randomInt(100, 9999)} ${
        ["Oak", "Pine", "Maple", "Cedar"][randomInt(0, 3)]
      } Street`,
      eventDate: randomDate().toISOString().split("T")[0],
      duration: `${randomInt(1, 8)} hours`,
      applicantName: ["Fire Dept.", "Event Organizer", "Property Owner"][
        randomInt(0, 2)
      ],
      safetyMeasures: [
        "Fire extinguisher on site",
        "Water source nearby",
        "Professional supervision",
      ][randomInt(0, 2)],
    },
    3: {
      // Info
      formType: "Information Request",
      requestType: [
        "Public Records",
        "Permit Status",
        "Zoning Information",
        "Property Tax",
      ][randomInt(0, 3)],
      subject: [
        "Property at 123 Main St",
        "Business License Status",
        "Zoning Variance",
        "Tax Assessment",
      ][randomInt(0, 3)],
      requesterName: [
        "Legal Firm",
        "Property Developer",
        "Citizen",
        "Business Owner",
      ][randomInt(0, 3)],
      purpose: [
        "Legal proceedings",
        "Due diligence",
        "Personal inquiry",
        "Business planning",
      ][randomInt(0, 3)],
      urgency: ["Standard", "Expedited", "Rush"][randomInt(0, 2)],
    },
  };

  const formType = formTypes[formId] || formTypes[1];
  return {
    ...formType,
    submissionNotes: `Additional notes for application submitted on ${new Date().toLocaleDateString()}`,
    attachments: randomInt(0, 3),
  };
};

export const generateRandomApplication = (id) => {
  const statuses = Object.values(ApplicationStatus);
  const status = statuses[randomInt(0, statuses.length - 1)];
  const formId = randomInt(1, 3); // Depends on the generateRandomJsonPayload and how many types there are disclosed in the function
  const hasPreviousSnapshot = Math.random() > 0.7;

  return {
    id: id,
    formId: formId,
    applicantId: randomInt(1000, 9999),
    adminId: randomInt(100, 999),
    status: status,
    createdAt: randomDate(),
    currentSnapshotId: randomInt(10000, 99999),
    previousSnapshotId: hasPreviousSnapshot ? randomInt(10000, 99999) : null,
    jsonPayload: generateRandomJsonPayload(formId),
  };
};

export const generateRandomApplications = (count = 10) => {
  const applications = [];
  for (let i = 1; i <= count; i++) {
    applications.push(generateRandomApplication(i));
  }
  return applications;
};

export const generateRandomApplicationsDict = (count = 10) => {
  const applications = {};
  for (let i = 1; i <= count; i++) {
    const app = generateRandomApplication(i);
    applications[app.id] = app;
  }
  return applications;
};

export const filterApplicationsByStatus = (applications, status) => {
  if (Array.isArray(applications)) {
    return applications.filter((app) => app.status === status);
  } else {
    const filtered = {};
    Object.keys(applications).forEach((key) => {
      if (applications[key].status === status) {
        filtered[key] = applications[key];
      }
    });
    return filtered;
  }
};

// Example usage:
// const singleApp = generateRandomApplication(1);
// const appsArray = generateRandomApplications(20);
// const appsDict = generateRandomApplicationsDict(15);
// const pendingApps = filterApplicationsByStatus(appsArray, ApplicationStatus.PENDING);
