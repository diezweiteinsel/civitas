import { render } from "@testing-library/react"
import ApplicationContainer from "../src/components/ApplicationContainer";


const mockApplication = [
    {
        id: 111,
        formId: 1,
        status: "pending"

    },

    {
        id: 112,
        forID: 2,
        status: "rejected"
    }
]

describe(ApplicationContainer, () => {
    
    it("correct icon is displayed based on form type", () => { //getIconByFormId
        const {} = render(<initialIcon/>)
    })
})

