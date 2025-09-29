import { render } from "@testing-library/react"
import ApplicationContainer from "../src/components/ApplicationContainer";


describe(ApplicationContainer, () => {
    
    it("correct icon is displayed based on form type", () => { //getIconByFormId
        const {} = render(<initialIcon/>)
    })
})

const mockApplication = [
    {
        id: 111,
        formId: 1

    },

    {
        id: 112,
        forID: 2
    }
]