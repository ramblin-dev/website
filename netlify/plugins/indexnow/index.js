module.exports = {
  onSuccess: async ({ utils }) => {
    if (process.env.CONTEXT !== 'production') {
      console.log(`Skipping IndexNow ping (CONTEXT=${process.env.CONTEXT || 'unset'})`);
      return;
    }
    await utils.run.command('./scripts/indexnow-ping.sh');
  },
};
