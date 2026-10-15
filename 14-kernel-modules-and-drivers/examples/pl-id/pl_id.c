// SPDX-License-Identifier: GPL-2.0-only
/* Teaching example: synthetic IP contract documented in section 14.04. */
#include <linux/io.h>
#include <linux/module.h>
#include <linux/of.h>
#include <linux/platform_device.h>
#include <linux/slab.h>
#include <linux/sysfs.h>

#define PL_ID_OFFSET 0x0
#define PL_ID_EXPECTED 0x504c4944

struct pl_id {
	void __iomem *base;
};

static ssize_t identity_show(struct device *dev,
			     struct device_attribute *attr, char *buf)
{
	struct pl_id *id = dev_get_drvdata(dev);

	return sysfs_emit(buf, "0x%08x\n", readl(id->base + PL_ID_OFFSET));
}
static DEVICE_ATTR_RO(identity);

static struct attribute *pl_id_attrs[] = {
	&dev_attr_identity.attr,
	NULL,
};
ATTRIBUTE_GROUPS(pl_id);

static int pl_id_probe(struct platform_device *pdev)
{
	struct resource *res;
	struct pl_id *id;
	u32 value;

	res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
	if (!res || resource_size(res) < sizeof(u32))
		return dev_err_probe(&pdev->dev, -EINVAL, "missing ID register\n");

	id = devm_kzalloc(&pdev->dev, sizeof(*id), GFP_KERNEL);
	if (!id)
		return -ENOMEM;

	id->base = devm_platform_ioremap_resource(pdev, 0);
	if (IS_ERR(id->base))
		return PTR_ERR(id->base);

	value = readl(id->base + PL_ID_OFFSET);
	if (value != PL_ID_EXPECTED)
		return dev_err_probe(&pdev->dev, -ENODEV,
				     "unexpected ID 0x%08x\n", value);

	platform_set_drvdata(pdev, id);
	return devm_device_add_groups(&pdev->dev, pl_id_groups);
}

static const struct of_device_id pl_id_match[] = {
	{ .compatible = "example,pl-id-v1" },
	{ }
};
MODULE_DEVICE_TABLE(of, pl_id_match);

static struct platform_driver pl_id_driver = {
	.probe = pl_id_probe,
	.driver = {
		.name = "pl-id",
		.of_match_table = pl_id_match,
	},
};
module_platform_driver(pl_id_driver);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Read-only synthetic PL identification example");
