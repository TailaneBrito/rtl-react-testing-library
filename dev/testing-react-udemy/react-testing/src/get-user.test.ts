import { getUser } from "./get-user"

describe('when everything is OK',  () => {
    test('should return a response', async () => {
        //mocking axios and getting the get method

        const result = await getUser();
        expect(result).toStrictEqual({ id: "1", name: "Tailane" })
    })
})